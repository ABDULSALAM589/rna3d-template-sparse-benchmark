# NuFold Setup

Verified Colab environment:

```text
Python 3.13.15
NumPy 2.1.3
PyTorch 2.11.0+cu130
CUDA True
GPU Tesla T4
Commit f77d34af97c1d0f88b47dd2f3c038004fe2ebe13
```

Installed dependencies:
`ml-collections dm-tree deepspeed protobuf scipy biopython numpy matplotlib py3Dmol`

Checkpoint:
`checkpoints/global_step145245.pt`

Observed checkpoint size:
`726.13 MB`

The official README notes older tested PyTorch versions, but this Colab verification succeeded with PyTorch 2.11.0+cu130.

The full rMSA database is intentionally excluded from this verification workflow because of its heavy storage requirements.
