# RhoFold+ Setup

Verified Colab environment:

```text
Python 3.7.12
NumPy 1.21.2
PyTorch 1.10.2
CUDA True
GPU Tesla T4
Commit 6bdfbda720184409eb682ce08c05d258162ddc48
```

The official repository environment also specifies CUDA 11.3 and OpenMM 7.7.

Checkpoint:
`pretrained/RhoFold_pretrained.pt`

Observed checkpoint size:
`484.77 MB`

The clean Colab notebook uses Micromamba and the repository-provided `envs/environment_linux.yaml`.

The automatic MSA database workflow is intentionally excluded from verification because the upstream README states that RNAcentral, Rfam and nt together require roughly 900 GB.
