# RNAbpFlow Inference

## Configuration

Default settings are in `configs/inference.yaml`.

Important fields include checkpoint path, input directory, output directory, GPU count, sample count and output format.

## Run

Inside the RNAbpFlow environment:

```bash
python inference.py
```

Verified Colab invocation:

```text
/content/bin/micromamba -r /content/micromamba_root run \
  -n RNAbpFlow python inference.py
```

## Verified Run

```text
Exit code: 0
Runtime: 60.32 s
Peak observed GPU memory: 641 MiB
```

Per-target completion:

```text
2oiu_P: 20.49 s
8tux_R: 32.04 s
```

The verified target list requested 5 samples for `2oiu_P` and 10 samples for `8tux_R`.

## Outputs

Predictions are generated under `Predictions/<target_id>/`.

RNAbpFlow can output PDB, mmCIF, or both depending on configuration.

## Final Benchmark Runs

1. Prepare target FASTA + predicted BP maps.
2. Fix the number of generated samples per target.
3. Run inference.
4. Record runtime, exit code, GPU, peak VRAM, commit and checkpoint.
5. Persist large outputs externally.
6. Evaluate generated structures with the common benchmark pipeline.
