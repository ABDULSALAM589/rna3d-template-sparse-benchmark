# RNAbpFlow

## Status

**READY — successful end-to-end Google Colab inference verified.**

RNAbpFlow is a base-pair-conditioned SE(3)-flow-matching model for RNA 3D structure generation.

## Upstream

- **Official repository:** https://github.com/Bhattacharya-Lab/RNAbpFlow
- **Paper:** Tarafder & Bhattacharya, Nature Methods (2026)
- **DOI:** 10.1038/s41592-026-03128-4
- **Verified upstream commit:** `e8b1c077f7951d4d6ebe00c851d22c37777dfc9f`

## Verified Colab Environment

- Python: 3.10
- NumPy: 1.26.4
- PyTorch: 2.1.2
- CUDA available: True
- GPU: Tesla T4
- Checkpoint: `RNA3DB.ckpt`
- Checkpoint size observed: ~193.63 MB

## Required Inputs

Per target:
- RNA sequence in FASTA format
- base-pair map input(s)

Official example layout:

```text
Inputs/<target_id>/
├── <target_id>.fasta
├── map1.npy
├── map2.npy
└── map3.npy
```

A single base-pair map may be replicated three times to match the required channel dimension.

## Verified Run

- Exit code: `0`
- Total measured runtime: `60.32 s`
- Peak observed GPU memory: `641 MiB`
- `2oiu_P`: `20.49 s`
- `8tux_R`: `32.04 s`

Predictions are written under `Predictions/<target_id>/`.

Outputs were also saved to:

```text
/content/drive/MyDrive/RNA3D_Benchmark/RNAbpFlow
```

## Benchmark Policy

1. Use the benchmark RNA sequence as FASTA input.
2. Use one fixed, documented predicted base-pair-map pipeline.
3. Do not use the native experimental 3D structure as inference input.
4. Do not use native/ground-truth base pairs in the primary benchmark.
5. Native BP maps may only be used in a separately labelled oracle experiment.
6. Record commit, checkpoint, runtime, GPU, peak VRAM and sample count.
7. Evaluate structures against native coordinates only after inference.

## Readiness

- [x] Official repository verified
- [x] Colab environment created
- [x] MKL compatibility issue resolved
- [x] NumPy compatibility issue resolved
- [x] CUDA/GPU verified
- [x] Checkpoint loaded
- [x] Example FASTA + BP maps processed
- [x] Multi-target inference successful
- [x] Structures generated
- [x] Runtime and peak GPU memory logged
- [x] Google Drive persistence verified
- [x] Reproducible Colab notebook prepared
- [ ] Final benchmark BP-map generation pipeline standardized
- [ ] Final benchmark sample-selection policy standardized
