# RhoFold+

## Status
**READY — successful end-to-end Google Colab inference verified.**

## Upstream
- Official repository: `ml4bio/RhoFold`
- Verified commit: `6bdfbda720184409eb682ce08c05d258162ddc48`
- Paper: Nature Methods (2024)
- DOI: `10.1038/s41592-024-02487-0`

## Verified Environment
- Python: 3.7.12
- NumPy: 1.21.2
- PyTorch: 1.10.2
- CUDA available: True
- GPU: Tesla T4
- Checkpoint: `RhoFold_pretrained.pt`
- Checkpoint size observed: 484.77 MB

## Verified Input
```text
example/input/3owzA/
├── 3owzA.fasta
└── 3owzA.a3m
```

## Verified Run
```text
Exit code: 0
Total runtime: 878.98 s
Peak observed GPU memory: 2659 MiB
RhoFold neural inference: 15.587 s
Amber relaxation (1000 iterations): 852.064 s
```

Primary verified output:
`example/output/3owzA_verify/relaxed_1000_model.pdb`

Generated files:
```text
log.txt
relaxed_1000_model.pdb
results.npz
ss.ct
unrelaxed_model.pdb
```

## Drive
Verified save path:
`/content/drive/MyDrive/RNA3D_Benchmark/RhoFold`

## Benchmark Policy
Primary benchmark mode is FASTA + standardized/precomputed A3M. Sequence-only mode is kept separate as an ablation/quick-reference condition.

## Readiness
- [x] Official repo verified
- [x] Official environment created
- [x] CUDA/GPU verified
- [x] Checkpoint downloaded
- [x] Bundled FASTA/A3M verified
- [x] GPU inference successful
- [x] Relaxed PDB generated
- [x] Runtime/VRAM logged
- [x] Drive save verified
- [x] Custom A3M workflow prepared
- [x] Sequence-only ablation workflow prepared
- [ ] Final benchmark MSA-generation policy standardized
