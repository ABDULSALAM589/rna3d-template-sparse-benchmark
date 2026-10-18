"""Small dependency-free helpers shared by the NuFold pilot scripts."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import tempfile
from pathlib import Path
from typing import Any


RNA_CODES = {"A": "A", "C": "C", "G": "G", "U": "U", "RA": "A", "RC": "C", "RG": "G", "RU": "U"}
THREE_TO_ONE = {"A": "A", "C": "C", "G": "G", "U": "U", "ADE": "A", "CYT": "C", "GUA": "G", "URA": "U"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def read_manifest(path: Path) -> list[dict[str, str]]:
    required = {"target_id", "pdb_id", "chain_id", "sequence", "length", "release_date", "template_screen_status"}
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"Pilot manifest is missing required columns: {sorted(required - set(reader.fieldnames or []))}")
        rows = list(reader)
    if not rows:
        raise ValueError("Pilot manifest contains no targets")
    ids = [row["target_id"].strip() for row in rows]
    if any(not re.fullmatch(r"[A-Za-z0-9_.-]+", target_id) for target_id in ids):
        raise ValueError("Manifest contains an unsafe target_id")
    if len(set(ids)) != len(ids):
        raise ValueError("Pilot manifest contains duplicate target IDs")
    for row in rows:
        seq = row["sequence"].strip().upper().replace("T", "U")
        if not seq or set(seq) - set("ACGU"):
            raise ValueError(f"{row['target_id']}: expected an A/C/G/U sequence")
        if len(seq) != int(row["length"]):
            raise ValueError(f"{row['target_id']}: manifest length does not match its sequence")
        row["sequence"] = seq
        row["target_id"] = row["target_id"].strip()
    return rows


def write_fasta(path: Path, target_id: str, sequence: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f">{target_id}\n{sequence}\n"
    _write_immutable(path, content)


def _write_immutable(path: Path, content: str) -> None:
    if path.exists():
        if path.read_text() != content:
            raise FileExistsError(f"Refusing to replace different existing input: {path}")
        return
    path.write_text(content)


def count_a3m_records(path: Path) -> int:
    count = sum(1 for line in path.read_text().splitlines() if line.startswith(">"))
    if count < 1:
        raise ValueError(f"No FASTA records in A3M: {path}")
    return count


def a3m_query_sequence(path: Path) -> str:
    sequence = []
    saw_header = False
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if saw_header:
                break
            saw_header = True
            continue
        if saw_header:
            sequence.append(line)
    if not saw_header:
        raise ValueError(f"A3M has no header: {path}")
    # A3M lower-case letters denote insertions; gaps are omitted for query comparison.
    return "".join(c for c in "".join(sequence) if c not in "-." and not c.islower()).upper().replace("T", "U")


def pdb_residues(path: Path) -> list[dict[str, Any]]:
    residues: list[dict[str, Any]] = []
    seen = set()
    for line in path.read_text(errors="replace").splitlines():
        if not line.startswith(("ATOM  ", "HETATM")) or len(line) < 26:
            continue
        alt = line[16:17]
        if alt not in (" ", "A", "1"):
            continue
        key = (line[21:22], line[22:26], line[26:27], line[17:20].strip())
        if key not in seen:
            seen.add(key)
            name = line[17:20].strip().upper()
            residues.append({"key": key, "chain": key[0], "resseq": key[1].strip(), "icode": key[2].strip(),
                             "name": name, "one": THREE_TO_ONE.get(name, RNA_CODES.get(name, "N"))})
    return residues


def validate_ranked_pdb(path: Path, expected_length: int) -> dict[str, Any]:
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"Missing/empty prediction PDB: {path}")
    lines = path.read_text(errors="replace").splitlines()
    atoms = [line for line in lines if line.startswith(("ATOM  ", "HETATM"))]
    residues = pdb_residues(path)
    if not atoms:
        raise ValueError(f"Prediction contains no coordinate records: {path}")
    if not residues:
        raise ValueError(f"Prediction contains no recognizable residues: {path}")
    if len(residues) != expected_length:
        raise ValueError(f"Prediction has {len(residues)} residues; expected {expected_length}: {path}")
    if any(r["one"] == "N" for r in residues):
        raise ValueError(f"Prediction contains an unrecognized nucleotide residue: {path}")
    for line in atoms:
        if len(line) < 54:
            raise ValueError(f"Truncated coordinate record in {path}")
        try:
            xyz = [float(line[start:end]) for start, end in ((30, 38), (38, 46), (46, 54))]
        except ValueError as exc:
            raise ValueError(f"Invalid coordinate in {path}: {line}") from exc
        if not all(math.isfinite(value) for value in xyz):
            raise ValueError(f"Non-finite coordinate in {path}")
    return {"residues": len(residues), "atoms": len(atoms), "sequence": "".join(r["one"] for r in residues)}


def write_mapped_prediction(source: Path, destination: Path, target_sequence: str,
                            observed_target_positions: list[int]) -> int:
    residues = pdb_residues(source)
    pred_seq = "".join(r["one"] for r in residues)
    if pred_seq != target_sequence:
        raise ValueError(f"Prediction sequence mismatch in {source}: {pred_seq} != {target_sequence}")
    wanted = set(observed_target_positions)
    if not wanted or min(wanted) < 1 or max(wanted) > len(target_sequence):
        raise ValueError("Native residue map contains invalid target positions")
    residue_lookup = {r["key"]: i + 1 for i, r in enumerate(residues)}
    mapped_lines = []
    serial = 1
    for line in source.read_text(errors="replace").splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        alt = line[16:17]
        if alt not in (" ", "A", "1"):
            continue
        key = (line[21:22], line[22:26], line[26:27], line[17:20].strip())
        target_pos = residue_lookup.get(key)
        if target_pos not in wanted:
            continue
        # Set residue numbering to target positions so it agrees with the native map.
        mapped_lines.append(line[:6] + f"{serial:5d}" + line[11:22] + f"{target_pos:4d}" + line[26:])
        serial += 1
    if not mapped_lines:
        raise ValueError(f"No mapped atoms retained from prediction: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(mapped_lines + ["TER", "END"]) + "\n")
    return len(wanted)


def read_native_positions(map_path: Path) -> list[int]:
    with map_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [int(r["target_position"]) for r in rows if r["coordinates_present"].lower() == "yes"]


def parse_usalign(text: str, native_coordinate_residues: int) -> dict[str, float | int]:
    import re

    common = re.search(r"Number of residues in common\s*=\s*(\d+)", text, re.I)
    rmsd = re.search(r"RMSD of the common residues\s*=\s*([0-9.eE+-]+)", text, re.I)
    tm = re.search(r"TM-score\s*=\s*([0-9.eE+-]+)", text, re.I)
    if not common or not rmsd or not tm:
        raise ValueError("Could not parse USalign common-residue count, RMSD, and TM-score")
    n_common = int(common.group(1))
    return {"alignment_residues": n_common, "alignment_coverage": n_common / native_coordinate_residues,
            "rmsd_angstrom": float(rmsd.group(1)), "tm_score": float(tm.group(1))}

