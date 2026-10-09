# trRosettaRNA2

## Status

**READY — successful end-to-end Google Colab inference verified.**

trRosettaRNA2 is an end-to-end RNA 3D structure prediction method that uses an RNA multiple-sequence alignment (MSA) and an internal secondary-structure prior module, trRNA2-SS.

## Upstream

- Official repository: `YangLab-SDU/trRosettaRNA2`
- Verified commit: `d40a40e36617cb4004a11b0a7603167415ed9c52`
- Paper: Nature Machine Intelligence (2026)
- DOI: `10.1038/s42256-026-01223-x`

## Verified Colab Environment

- Host Python: 3.13.15
- Model environment Python: 3.10.14
- NumPy: 2.1.2
- PyTorch: 2.5.1
- CUDA available: True
- GPU: Tesla T4
- PyRosetta: 2024.39+release.59628fb

## Primary Input

The standalone pipeline requires an A3M MSA:

```text
example/seq.a3m
```

Custom secondary structure is optional. If none is provided, the model uses internal `trRNA2-SS`.

## Verified Run

```text
Exit code: 0
Runtime: 30.06 s
Peak observed GPU memory: 351 MiB
pLDDT: 0.920
```

Verified final output:

```text
example/output/model_1_relaxed200.pdb
```

Additional generated files included:

```text
model_1.pdb
model_1_2D.npz
model_1_ref200.pdb
model_1_relaxed200.pdb
model_1_unrelaxed.pdb
plddt.csv
```

Outputs were also saved to:

```text
/content/drive/MyDrive/RNA3D_Benchmark/trRosettaRNA2
```

## Benchmark Policy

For the primary benchmark:

1. Generate target-specific A3M input using one standardized MSA-generation policy.
2. Use internal `trRNA2-SS`.
3. Do not use native experimental 3D coordinates during inference.
4. Reserve native structure for evaluation only.
5. Treat custom/native SS runs as separately labelled ablation/oracle experiments.
6. Record model commit, runtime, GPU, peak VRAM and output path.

For team reproducibility, precomputed A3M files should be shared so every member does not need the optional ~32 GB RNAcentral database.

## Readiness

- [x] Official repository verified
- [x] Official environment created
- [x] CUDA/GPU verified
- [x] Official weights downloaded
- [x] Bundled A3M input verified
- [x] Inference successful
- [x] Relaxed PDB generated
- [x] Runtime logged
- [x] Peak GPU memory logged
- [x] Google Drive save verified
- [x] Reproducible Colab notebook prepared
- [ ] Final benchmark MSA-generation pipeline standardized
