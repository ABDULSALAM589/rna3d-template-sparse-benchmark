#!/usr/bin/env python3
"""Resume-safe NuFold batch inference and post-inference evaluation runner."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

from common import atomic_json, count_a3m_records, read_manifest, sha256_file, write_fasta, a3m_query_sequence, validate_ranked_pdb
from evaluate import evaluate_ranked


REPO_ROOT = Path(__file__).resolve().parents[2]
SUMMARY_FIELDS = ["target_id", "status", "msa_type", "msa_sequences", "runtime_seconds", "peak_gpu_memory_mib_observed",
                  "ranked_outputs", "native_status", "rank", "alignment_coverage", "tm_score", "rmsd_angstrom", "error"]


def load_config(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text())
    base = path.resolve().parent.parent
    for key in ("manifest", "native_eval_dir"):
        if key in config:
            p = Path(config[key])
            config[key] = str((base / p).resolve() if not p.is_absolute() else p)
    return config


def gpu_info() -> tuple[str | None, int | None]:
    binary = shutil.which("nvidia-smi")
    if not binary:
        return None, None
    try:
        name = subprocess.check_output([binary, "--query-gpu=name", "--format=csv,noheader"], text=True, timeout=10).splitlines()[0].strip()
        memory = int(subprocess.check_output([binary, "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                                             text=True, timeout=10).splitlines()[0].strip())
        return name, memory
    except Exception:
        return None, None


def require_cuda(python: str) -> dict[str, Any]:
    code = "import json,torch; print(json.dumps({'cuda':torch.cuda.is_available(),'gpu':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,'torch':torch.__version__}))"
    p = subprocess.run([python, "-c", code], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(f"Unable to inspect PyTorch/CUDA with {python}: {p.stderr.strip()}")
    info = json.loads(p.stdout.strip().splitlines()[-1])
    if not info["cuda"]:
        raise RuntimeError("CUDA is unavailable; no NuFold inference was started")
    return info


def prepare_a3m(target: dict[str, str], msa_mode: str, source_dir: Path | None, destination: Path) -> int:
    target_id, sequence = target["target_id"], target["sequence"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    if msa_mode == "single_sequence":
        content = f">{target_id}\n{sequence}\n"
        if destination.exists() and destination.read_text() != content:
            raise FileExistsError(f"Refusing to replace different A3M: {destination}")
        if not destination.exists():
            destination.write_text(content)
        return 1
    if msa_mode != "genuine":
        raise ValueError(f"Unsupported MSA mode: {msa_mode}")
    if source_dir is None:
        raise ValueError("--msa-source-dir is required for genuine MSA mode")
    source = locate_genuine_a3m(target_id, source_dir)
    query = a3m_query_sequence(source)
    if query != sequence:
        raise ValueError(f"{target_id}: A3M query does not match manifest sequence")
    count = count_a3m_records(source)
    if count < 2:
        raise ValueError(f"{target_id}: genuine MSA mode requires at least two aligned records; found {count}")
    content = source.read_text()
    if destination.exists() and destination.read_text() != content:
        raise FileExistsError(f"Refusing to replace different A3M in this run: {destination}")
    if not destination.exists():
        destination.write_text(content)
    return count


def locate_genuine_a3m(target_id: str, source_dir: Path) -> Path:
    options = [source_dir / f"{target_id}.a3m", source_dir / target_id / f"{target_id}.a3m"]
    source = next((p for p in options if p.is_file()), None)
    if source is None:
        raise FileNotFoundError(f"No genuine MSA for {target_id}; expected one of: {options}")
    return source


def install_ss(target: dict[str, str], fasta: Path, ss_path: Path, ipknot: Path) -> str:
    if ss_path.is_file() and ss_path.stat().st_size:
        return "reused_existing_in_run"
    ss_path.parent.mkdir(parents=True, exist_ok=True)
    with ss_path.open("w") as handle:
        proc = subprocess.run([str(ipknot), str(fasta)], stdout=handle, stderr=subprocess.PIPE, text=True)
    if proc.returncode or ss_path.stat().st_size == 0:
        raise RuntimeError(f"IPknot failed for {target['target_id']} (exit {proc.returncode}): {proc.stderr[-1500:]}")
    return "generated_by_ipknot"


def input_files_only(input_root: Path) -> None:
    forbidden_suffixes = (".pdb", ".ent", ".cif", ".mmcif", ".pdb.gz", ".cif.gz", ".mmcif.gz")
    forbidden = [p for p in input_root.rglob("*") if p.is_file() and p.name.lower().endswith(forbidden_suffixes)]
    if forbidden:
        raise RuntimeError("Native/coordinate files are forbidden in the NuFold input tree: " + ", ".join(map(str, forbidden)))


def sample_gpu(stop: threading.Event, samples: list[int]) -> None:
    binary = shutil.which("nvidia-smi")
    if not binary:
        return
    while not stop.is_set():
        try:
            out = subprocess.check_output([binary, "--query-gpu=memory.used", "--format=csv,noheader,nounits"], text=True, timeout=5)
            values = [int(line.strip()) for line in out.splitlines() if line.strip()]
            if values:
                samples.append(max(values))
        except Exception:
            pass
        stop.wait(0.5)


def write_summary(run_dir: Path) -> None:
    records_dir = run_dir / "records"
    rows = []
    for path in sorted(records_dir.glob("*.json")):
        record = json.loads(path.read_text())
        base = {key: record.get(key) for key in SUMMARY_FIELDS}
        eval_rows = record.get("evaluation", []) or [{}]
        for ev in eval_rows:
            rows.append({**base, "rank": ev.get("rank"), "alignment_coverage": ev.get("alignment_coverage"),
                         "tm_score": ev.get("tm_score"), "rmsd_angstrom": ev.get("rmsd_angstrom")})
    temp = run_dir / "summary.csv.tmp"
    with temp.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp, run_dir / "summary.csv")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=REPO_ROOT / "configs/nufold_pilot.json")
    ap.add_argument("--run-id", default=None, help="Use a stable ID to resume the same run")
    ap.add_argument("--resume", action="store_true", help="Resume an existing run ID; completed targets are checksum-verified and skipped")
    ap.add_argument("--msa-mode", choices=["single_sequence", "genuine"], default=None)
    ap.add_argument("--msa-source-dir", type=Path, default=None)
    ap.add_argument("--msa-provenance", default=None, help="Database/tool/version/date/settings for genuine MSA input")
    ap.add_argument("--run-root", type=Path, default=None)
    ap.add_argument("--nufold-root", type=Path, default=None)
    ap.add_argument("--checkpoint", type=Path, default=None)
    ap.add_argument("--ipknot", type=Path, default=None)
    ap.add_argument("--usalign", type=Path, default=None)
    ap.add_argument("--targets", nargs="*", help="Optional subset of IDs from the manifest; no new IDs are accepted")
    args = ap.parse_args()

    cfg = load_config(args.config)
    manifest = Path(cfg["manifest"])
    nufold_root = (args.nufold_root or Path(cfg["nufold_root"])).resolve()
    checkpoint = (args.checkpoint or Path(cfg["checkpoint"])).resolve()
    ipknot = (args.ipknot or Path(cfg["ipknot"])).resolve()
    usalign = args.usalign or Path(cfg["usalign"])
    native_dir = Path(cfg["native_eval_dir"])
    run_root = (args.run_root or Path(cfg["run_root"])).resolve()
    msa_mode = args.msa_mode or cfg.get("msa_mode", "single_sequence")
    msa_source_dir = args.msa_source_dir or (Path(cfg["msa_source_dir"]) if cfg.get("msa_source_dir") else None)
    msa_provenance = ("single-sequence baseline; generated from manifest sequence" if msa_mode == "single_sequence"
                      else (args.msa_provenance or cfg.get("msa_provenance")))
    if msa_mode == "genuine" and not msa_provenance:
        raise ValueError("--msa-provenance is required in genuine MSA mode")
    python = cfg.get("python", sys.executable)
    run_id = args.run_id or dt.datetime.now(dt.timezone.utc).strftime("nufold_%Y%m%dT%H%M%SZ")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", run_id):
        raise ValueError("Unsafe run_id")
    run_dir = run_root / run_id
    if args.resume:
        if not run_dir.is_dir():
            raise FileNotFoundError(f"Cannot resume; run directory does not exist: {run_dir}")

    rows = read_manifest(manifest)
    if args.targets:
        unknown = sorted(set(args.targets) - {r["target_id"] for r in rows})
        if unknown:
            raise ValueError(f"Targets are not in the pilot manifest: {unknown}")
        rows = [row for row in rows if row["target_id"] in set(args.targets)]
    if not rows:
        raise ValueError("No manifest targets selected")
    if not checkpoint.is_file():
        raise FileNotFoundError(f"NuFold checkpoint not found: {checkpoint}")
    nufold_script = nufold_root / "run_nufold.py"
    if not nufold_script.is_file():
        raise FileNotFoundError(f"NuFold entrypoint not found: {nufold_script}")
    if not ipknot.is_file():
        raise FileNotFoundError(f"IPknot executable not found: {ipknot}")
    cuda = require_cuda(python)
    try:
        commit = subprocess.check_output(["git", "-C", str(nufold_root), "rev-parse", "HEAD"], text=True).strip()
    except Exception as exc:
        raise RuntimeError(f"Could not determine NuFold Git commit: {exc}")
    a3m_sources = {}
    if msa_mode == "genuine":
        if msa_source_dir is None:
            raise ValueError("--msa-source-dir is required for genuine MSA mode")
        for target in rows:
            source = locate_genuine_a3m(target["target_id"], msa_source_dir)
            query = a3m_query_sequence(source)
            if query != target["sequence"] or count_a3m_records(source) < 2:
                raise ValueError(f"{target['target_id']}: genuine MSA query mismatch or alignment depth < 2")
            a3m_sources[target["target_id"]] = {"path": str(source.resolve()), "sha256": sha256_file(source),
                                                 "records": count_a3m_records(source)}
    immutable = {"manifest_sha256": sha256_file(manifest), "msa_mode": msa_mode,
                 "model_commit": commit, "checkpoint_sha256": sha256_file(checkpoint),
                 "checkpoint": str(checkpoint), "config_preset": cfg.get("config_preset", "initial_training"),
                 "ipknot_sha256": sha256_file(ipknot),
                 "msa_provenance": msa_provenance, "target_ids": [r["target_id"] for r in rows],
                 "a3m_sources": a3m_sources}
    run_meta = run_dir / "run.json"
    if args.resume:
        previous = json.loads(run_meta.read_text())
        for key, value in immutable.items():
            if previous.get(key) != value:
                raise RuntimeError(f"Resume configuration changed ({key}); use a new run ID to preserve completed work")
    else:
        run_dir.mkdir(parents=True, exist_ok=False)
        atomic_json(run_meta, {**immutable, "run_id": run_id, "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                               "cuda": cuda, "nufold_root": str(nufold_root), "ipknot": str(ipknot),
                               "msa_source_dir": str(msa_source_dir) if msa_source_dir else None})

    input_root, output_root = run_dir / "inputs", run_dir / "outputs"
    (run_dir / "records").mkdir(parents=True, exist_ok=True)
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    input_root.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)
    for target in rows:
        target_id, sequence = target["target_id"], target["sequence"]
        record_path = run_dir / "records" / f"{target_id}.json"
        output_dir = output_root / target_id
        prior = json.loads(record_path.read_text()) if record_path.exists() else {}
        if args.resume and prior.get("status") == "complete":
            valid = True
            for artifact in prior.get("outputs", []):
                p = Path(artifact["path"])
                if not p.is_file() or sha256_file(p) != artifact["sha256"]:
                    valid = False
                    break
            if not valid:
                raise RuntimeError(f"Completed outputs changed/missing for {target_id}; preserving them, start a new run ID")
            print(f"SKIP completed {target_id}")
            continue

        target_input = input_root / target_id
        fasta = target_input / f"{target_id}.fasta"
        a3m = target_input / f"{target_id}.a3m"
        ss = target_input / f"{target_id}.single.ipknot.ss"
        try:
            write_fasta(fasta, target_id, sequence)
            msa_count = prepare_a3m(target, msa_mode, msa_source_dir, a3m)
            ss_mode = install_ss(target, fasta, ss, ipknot)
            input_root_files = sorted(str(p.relative_to(run_dir)) for p in target_input.iterdir() if p.is_file())
            if set(p.name for p in target_input.iterdir() if p.is_file()) != {fasta.name, a3m.name, ss.name}:
                raise RuntimeError(f"Unexpected files in NuFold input directory for {target_id}")
            input_files_only(input_root)
            input_hashes = {f.name: sha256_file(f) for f in (fasta, a3m, ss)}
            invariant_input = {"input_hashes": input_hashes, "msa_mode": msa_mode}
            if prior and prior.get("input_hashes") and prior["input_hashes"] != input_hashes:
                raise RuntimeError(f"Prepared inputs changed on resume for {target_id}; use a new run ID")
            atomic_json(record_path, {**prior, **invariant_input, "target_id": target_id, "status": "running",
                                      "sequence_length": len(sequence), "msa_type": "single_sequence_baseline" if msa_mode == "single_sequence" else "genuine_msa",
                                      "msa_sequences": msa_count, "secondary_structure": ss_mode,
                                      "msa_provenance": msa_provenance,
                                      "msa_source": a3m_sources.get(target_id, {}).get("path", "generated single-sequence A3M"),
                                      "msa_source_sha256": a3m_sources.get(target_id, {}).get("sha256"),
                                      "model_commit": commit, "checkpoint": str(checkpoint),
                                      "checkpoint_sha256": immutable["checkpoint_sha256"], "native_status": "available" if (native_dir / f"{target_id}_native_eval.pdb").is_file() else "native_unavailable",
                                      "ipknot_sha256": immutable["ipknot_sha256"],
                                      "input_files": input_root_files})
            samples: list[int] = []
            stop = threading.Event()
            monitor = threading.Thread(target=sample_gpu, args=(stop, samples), daemon=True)
            monitor.start()
            start = time.perf_counter()
            start_utc = dt.datetime.now(dt.timezone.utc).isoformat()
            cmd = [python, str(nufold_script), "--ckpt_path", str(checkpoint), "--input_fasta", str(fasta),
                   "--input_dir", str(input_root), "--output_dir", str(output_root), "--config_preset", immutable["config_preset"]]
            proc = subprocess.run(cmd, cwd=nufold_root, text=True, capture_output=True)
            elapsed = time.perf_counter() - start
            end_utc = dt.datetime.now(dt.timezone.utc).isoformat()
            stop.set(); monitor.join(timeout=3)
            log_path = run_dir / "logs" / f"{target_id}.log"
            log_path.write_text("$ " + " ".join(cmd) + "\n\n--- stdout ---\n" + proc.stdout + "\n--- stderr ---\n" + proc.stderr)
            ranked = sorted(output_dir.glob(f"{target_id}_rank_*.pdb"))
            outputs = []
            errors = []
            for pdb in ranked:
                try:
                    validation = validate_ranked_pdb(pdb, len(sequence))
                    if validation["sequence"] != sequence:
                        raise ValueError(f"Prediction sequence does not match manifest for {target_id}: {validation['sequence']}")
                    outputs.append({"path": str(pdb), "sha256": sha256_file(pdb), **validation})
                except Exception as exc:
                    errors.append(str(exc))
            status = "complete" if proc.returncode == 0 and outputs else "failed"
            try:
                evaluation = evaluate_ranked(target_id, sequence, output_dir, native_dir, usalign,
                                             run_dir / "evaluations" / target_id) if outputs else []
            except Exception as exc:
                evaluation = [{"target_id": target_id, "rank": None, "status": "evaluation_failed", "reason": str(exc)}]
            record = {**json.loads(record_path.read_text()), "status": status, "exit_code": proc.returncode,
                      "runtime_seconds": round(elapsed, 3), "peak_gpu_memory_mib_observed": max(samples) if samples else None,
                      "gpu": cuda.get("gpu"), "torch_version": cuda.get("torch"), "start_utc": start_utc,
                      "end_utc": end_utc, "outputs": outputs, "ranked_outputs": len(outputs),
                      "output_validation_errors": errors, "evaluation": evaluation,
                      "log": str(log_path), "error": None if status == "complete" else f"exit={proc.returncode}; {errors}"}
            atomic_json(record_path, record)
            write_summary(run_dir)
            print(f"{status.upper()} {target_id}: {len(outputs)} ranked structures; {elapsed:.2f}s; MSA={record['msa_type']}({msa_count})")
        except Exception as exc:
            failure = {**prior, "target_id": target_id, "status": "failed", "error": str(exc),
                       "model_commit": commit, "checkpoint_sha256": immutable["checkpoint_sha256"]}
            atomic_json(record_path, failure)
            write_summary(run_dir)
            print(f"FAILED {target_id}: {exc}", file=sys.stderr)
    print(f"Run records and outputs: {run_dir}")
    failed = []
    for target in rows:
        p = run_dir / "records" / f"{target['target_id']}.json"
        if not p.is_file() or json.loads(p.read_text()).get("status") != "complete":
            failed.append(target["target_id"])
    if failed:
        print("Targets failed inference/input preparation:", ", ".join(failed), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

