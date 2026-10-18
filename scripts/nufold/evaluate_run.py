#!/usr/bin/env python3
"""Re-evaluate a completed NuFold run when native structures/USalign become available."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
from pathlib import Path

from common import atomic_json, read_manifest
from evaluate import evaluate_ranked


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", required=True, type=Path)
    ap.add_argument("--config", type=Path, default=ROOT / "configs/nufold_pilot.json")
    ap.add_argument("--usalign", type=Path, default=None)
    ap.add_argument("--native-dir", type=Path, default=None)
    ap.add_argument("--evaluation-id", default=None)
    args = ap.parse_args()
    config = json.loads(args.config.read_text())
    config_base = args.config.resolve().parent.parent
    native_config = Path(config["native_eval_dir"])
    manifest_config = Path(config["manifest"])
    native_dir = args.native_dir or (native_config if native_config.is_absolute() else config_base / native_config)
    usalign = args.usalign or Path(config["usalign"])
    manifest = manifest_config if manifest_config.is_absolute() else config_base / manifest_config
    rows = read_manifest(manifest)
    run_meta = json.loads((args.run_dir / "run.json").read_text())
    eval_id = args.evaluation_id or dt.datetime.now(dt.timezone.utc).strftime("eval_%Y%m%dT%H%M%SZ")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", eval_id):
        raise ValueError("Unsafe evaluation ID")
    eval_root = args.run_dir / "evaluations" / eval_id
    eval_root.mkdir(parents=True, exist_ok=False)
    all_results = []
    for target in rows:
        target_id = target["target_id"]
        record_path = args.run_dir / "records" / f"{target_id}.json"
        if not record_path.is_file():
            all_results.append({"target_id": target_id, "rank": "", "status": "inference_not_run", "reason": "target record is absent"})
            continue
        record = json.loads(record_path.read_text())
        if record.get("status") != "complete":
            all_results.append({"target_id": target_id, "rank": "", "status": "inference_not_complete", "reason": record.get("error")})
            continue
        result = evaluate_ranked(target_id, target["sequence"], args.run_dir / "outputs" / target_id,
                                 native_dir, usalign, eval_root / target_id)
        for item in result:
            all_results.append({"target_id": target_id, **item,
                                "model_commit": run_meta.get("model_commit"),
                                "checkpoint_sha256": run_meta.get("checkpoint_sha256"),
                                "inference_runtime_seconds": record.get("runtime_seconds")})
    fields = ["target_id", "rank", "status", "native_residues", "alignment_residues", "alignment_coverage",
              "tm_score", "rmsd_angstrom", "inference_runtime_seconds", "model_commit", "checkpoint_sha256",
              "prediction", "mapped_prediction", "usalign_log", "reason"]
    csv_path = eval_root / "evaluation.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_results)
    atomic_json(eval_root / "evaluation.json", {"evaluation_id": eval_id, "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                                                 "run_dir": str(args.run_dir.resolve()), "native_dir": str(native_dir.resolve()),
                                                 "usalign": str(usalign), "results": all_results})
    print(f"Evaluation results: {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

