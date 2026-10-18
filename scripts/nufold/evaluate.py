"""Evaluation-only helpers for NuFold ranked RNA structures."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from common import parse_usalign, pdb_residues, read_native_positions, write_mapped_prediction


def evaluate_ranked(target_id: str, sequence: str, prediction_dir: Path,
                    native_dir: Path, usalign: Path, artifact_dir: Path | None = None) -> list[dict[str, Any]]:
    native_path = native_dir / f"{target_id}_native_eval.pdb"
    map_path = native_dir / f"{target_id}_residue_map.csv"
    if not native_path.is_file() or not map_path.is_file():
        return [{"target_id": target_id, "rank": None, "status": "native_unavailable",
                 "reason": "validated native PDB or residue-map sidecar is absent"}]
    if not usalign.is_file() and not _on_path(usalign):
        return [{"target_id": target_id, "rank": None, "status": "usalign_unavailable",
                 "reason": f"USalign executable not found: {usalign}"}]

    positions = read_native_positions(map_path)
    native_residues = pdb_residues(native_path)
    expected_native = "".join(sequence[pos - 1] for pos in positions)
    native_sequence = "".join(r["one"] for r in native_residues)
    if native_sequence != expected_native:
        raise ValueError(f"{target_id}: native sequence/map mismatch: {native_sequence} != {expected_native}")

    predictions = sorted(prediction_dir.glob(f"{target_id}_rank_*.pdb"))
    if not predictions:
        return [{"target_id": target_id, "rank": None, "status": "no_ranked_outputs",
                 "reason": "NuFold emitted no ranked PDB files"}]
    records = []
    artifact_dir = artifact_dir or prediction_dir / "evaluation_mapped"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    for prediction in predictions:
        rank = None
        try:
            rank = int(prediction.stem.rsplit("_rank_", 1)[1])
            mapped = artifact_dir / f"{prediction.stem}_mapped.pdb"
            write_mapped_prediction(prediction, mapped, sequence, positions)
            proc = subprocess.run([str(usalign), str(mapped), str(native_path), "-mol", "RNA", "-TMscore", "1"],
                                  check=False, capture_output=True, text=True)
            log_path = artifact_dir / f"{prediction.stem}_usalign.txt"
            log_path.write_text(proc.stdout + ("\n--- STDERR ---\n" + proc.stderr if proc.stderr else ""))
            if proc.returncode:
                raise RuntimeError(f"USalign exited {proc.returncode}: {proc.stderr[-1000:]}")
            metrics = parse_usalign(proc.stdout, len(native_residues))
            records.append({"target_id": target_id, "rank": rank, "status": "scored",
                            "native_residues": len(native_residues), "prediction": prediction.name,
                            "mapped_prediction": str(mapped), "usalign_log": str(log_path), **metrics})
        except Exception as exc:
            records.append({"target_id": target_id, "rank": rank, "status": "evaluation_failed",
                            "prediction": prediction.name, "reason": str(exc)})
    return records


def _on_path(path: Path) -> bool:
    import shutil
    return shutil.which(str(path)) is not None

