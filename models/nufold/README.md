# NuFold

## Status
**READY — successful end-to-end Google Colab inference verified.**

## Upstream
- Official repository: `kiharalab/NuFold`
- Verified commit: `f77d34af97c1d0f88b47dd2f3c038004fe2ebe13`
- Paper: Nature Communications (2025)
- DOI: `10.1038/s41467-025-56261-7`

## Verified Colab Environment
- Python: 3.13.15
- NumPy: 2.1.3
- PyTorch: 2.11.0+cu130
- CUDA: True
- GPU: Tesla T4
- Checkpoint: `global_step145245.pt`
- Checkpoint size: 726.13 MB

## Required Inputs

```text
TARGET/
├── TARGET.fasta
├── TARGET.a3m
└── TARGET.single.ipknot.ss
```

## Verified Run

```text
Exit code: 0
Runtime: 52.47 s
Peak observed GPU memory: 1231 MiB
```

Primary output:
`test_output/2DER_C/2DER_C_rank_1.pdb`

The run generated five ranked PDBs plus pLDDT plot and pickle artifacts.

## Google Drive

Verified save path:
`/content/drive/MyDrive/RNA3D_Benchmark/NuFold`

## Benchmark Policy

Use one standardized MSA-generation method and one standardized predicted-SS method across all benchmark targets. Native 3D and native SS must not be used as primary inference inputs.

## Readiness
- [x] Repo verified
- [x] Dependencies installed
- [x] GPU verified
- [x] Checkpoint downloaded
- [x] Bundled FASTA/A3M/SS verified
- [x] Inference successful
- [x] Ranked PDBs generated
- [x] Runtime/VRAM logged
- [x] Drive save verified
- [x] Custom-target workflow prepared
- [ ] Final benchmark MSA policy standardized
- [ ] Final benchmark SS policy standardized
