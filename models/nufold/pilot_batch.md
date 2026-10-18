# NuFold 10-Target Pilot Batch

This workflow uses the frozen `data/pilot/rna3d_template_sparse_pilot_v1.csv` without adding or substituting target IDs or sequences. That pilot CSV is an external dataset and is intentionally not included in the automation commit; supply the existing file through Drive or the Colab upload prompt. It calls the verified NuFold interface from `notebooks/nufold_colab.ipynb` and keeps native structures in a separate evaluation-only directory.

## Modes and inputs

For each target, the runner materializes:

```text
<run>/inputs/<TARGET>/<TARGET>.fasta
<run>/inputs/<TARGET>/<TARGET>.a3m
<run>/inputs/<TARGET>/<TARGET>.single.ipknot.ss
```

- `single_sequence`: writes a one-record A3M from the manifest sequence. This is explicitly logged as `single_sequence_baseline`; it is not a searched or genuine MSA.
- `genuine`: copies a precomputed A3M from `<msa-source-dir>/<TARGET>.a3m` or `<msa-source-dir>/<TARGET>/<TARGET>.a3m`. It validates that the query matches the pilot sequence and that at least two alignment records exist. Record the search database, version, date, and settings in the run's `run.json`/provenance field. The full rMSA database is about 2 TB in NuFold's upstream instructions, so the Colab launcher does not create a new MSA database automatically.
- Both modes generate predicted secondary structure by running IPknot on the manifest FASTA. No native SS or native coordinates are read for input preparation.

## Colab setup

Open [`notebooks/nufold_pilot_batch_colab.ipynb`](../../notebooks/nufold_pilot_batch_colab.ipynb) in Colab, select a GPU runtime, and run its cells top to bottom. For a private repository, create a Colab Secret named `GITHUB_TOKEN` with a fine-grained read-only Contents permission and enable access to it. The launcher uses Git's askpass mechanism so the token is not embedded in a URL or command and is never printed. Alternatively, download the private repository ZIP while signed in and upload it when prompted. The frozen pilot manifest remains a separate dataset: place the existing CSV at `MyDrive/RNA3D_Benchmark/rna3d_template_sparse_pilot_v1.csv` or upload it at the prompt. Required code, config, tests, and manifest are checked before expensive dependency installation. The notebook then checks out NuFold commit `f77d34af97c1d0f88b47dd2f3c038004fe2ebe13`, downloads checkpoint `global_step145245.pt`, installs IPknot 1.1.0 and builds USalign, then starts the batch runner. It refuses to proceed if PyTorch reports no CUDA GPU.

The output root is under mounted Google Drive, so inputs, predictions, logs, per-target JSON records, and summary CSV are written directly to Drive:

```text
MyDrive/RNA3D_Benchmark/NuFold/runs/<RUN_ID>/
├── inputs/
├── outputs/<TARGET>/<TARGET>_rank_*.pdb
├── records/<TARGET>.json
├── logs/<TARGET>.log
├── run.json
└── summary.csv
```

The native reference and residue map are read from `data/pilot/native_eval/` only after a prediction output has passed validation. `9cf2_W` has a mapped native PDB; other targets without both native PDB and map receive `native_unavailable` status and remain valid inference targets. Nothing under `native_eval/` is copied into `inputs/` or passed to `run_nufold.py`.

## Exact commands

After NuFold, checkpoint, IPknot, and USalign setup, a new single-sequence baseline run is:

```bash
cd "/content/rna3d-template-sparse-benchmark"
python scripts/nufold/run_batch.py \
  --config configs/nufold_pilot.json \
  --run-id pilot10_single_20261019 \
  --msa-mode single_sequence \
  --run-root "/content/drive/MyDrive/RNA3D_Benchmark/NuFold/runs" \
  --nufold-root /content/NuFold \
  --checkpoint /content/NuFold/checkpoints/global_step145245.pt \
  --ipknot /content/ipknot \
  --usalign /usr/local/bin/USalign
```

To resume that exact run after a Colab interruption, rerun with the same `--run-id` and add `--resume`. Completed targets are checksum-verified and skipped. A fresh run must use a new run ID; the runner refuses to reuse an existing ID unless `--resume` is explicit. Changed manifest, MSA mode, NuFold commit, or checkpoint hash blocks resume. Different inputs or settings belong in a new run.

For genuine MSAs, first put one correctly query-matched A3M per target in a Drive folder, then run:

```bash
python scripts/nufold/run_batch.py \
  --config configs/nufold_pilot.json \
  --run-id pilot10_genuine_20261019 \
  --msa-mode genuine \
  --msa-source-dir "/content/drive/MyDrive/RNA3D_Benchmark/MSA/pilot_v1" \
  --msa-provenance "<database, release, search tool/version, date, parameters>" \
  --run-root "/content/drive/MyDrive/RNA3D_Benchmark/NuFold/runs" \
  --nufold-root /content/NuFold \
  --checkpoint /content/NuFold/checkpoints/global_step145245.pt \
  --ipknot /content/ipknot \
  --usalign /usr/local/bin/USalign
```

The runner can also be called with `--targets 9cf2_W` to run a manifest-listed subset; it rejects unrecognized IDs. CPU-local tests exercise manifest, A3M, residue mapping, output parsing, and resume-safe file handling without starting NuFold.

If native files arrive after inference or you need to rerun evaluation with a newer USalign build, evaluate an existing run without rerunning inference:

```bash
python scripts/nufold/evaluate_run.py \
  --run-dir "/content/drive/MyDrive/RNA3D_Benchmark/NuFold/runs/<RUN_ID>" \
  --evaluation-id usalign_20261019
```

This writes a new immutable evaluation subdirectory and leaves prediction outputs and inference records untouched.

## Output handling and evaluation

For each target, the runner invokes the repository-documented command:

```bash
python run_nufold.py \
  --ckpt_path <checkpoint> \
  --input_fasta <run>/inputs/<TARGET>/<TARGET>.fasta \
  --input_dir <run>/inputs \
  --output_dir <run>/outputs \
  --config_preset initial_training
```

Primary outputs follow `<run>/outputs/<TARGET>/<TARGET>_rank_1.pdb`; all valid ranked PDBs are retained. PDBs are checked for coordinate records, recognized RNA residues, and expected sequence length. Each per-target JSON stores manifest/input hashes, MSA mode and depth, IPknot status, NuFold Git commit, checkpoint hash, runtime, GPU name, observed peak GPU memory, outputs/hashes, native availability, and per-rank evaluation records. `summary.csv` is refreshed after every target.

For evaluation, the native residue-map sidecar identifies the observed target positions. The runner checks prediction sequence against the manifest, trims prediction coordinates to those same positions, then calls `USalign <mapped prediction> <native> -mol RNA -TMscore 1` for known residue correspondence. It logs TM-score, RMSD, common residue count, and alignment coverage. Missing native files or missing USalign do not block inference; the target is recorded as unscored with a reason. Native and mapped evaluation files stay under `native_eval/` or each prediction's evaluation subdirectory, never under the model input tree.

NuFold's upstream readme describes the FASTA/A3M/secondary-structure folder contract and CLI; this implementation follows the environment and naming used by the repository's verified Colab notebook, including `.single.ipknot.ss`.
