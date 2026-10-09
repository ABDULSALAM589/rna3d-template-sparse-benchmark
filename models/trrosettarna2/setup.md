# trRosettaRNA2 Setup

## Verified Platform

```text
Platform: Google Colab
Host Python: 3.13.15
Environment Python: 3.10.14
NumPy: 2.1.2
PyTorch: 2.5.1
CUDA available: True
GPU: Tesla T4
Micromamba: 2.9.0
Commit: d40a40e36617cb4004a11b0a7603167415ed9c52
```

## Official Environment

The repository provides `environment.yml` with:

- Python 3.10
- NumPy 2.1.2
- PyRosetta 2024.39+release.59628fb
- CUDA toolkit 11.8
- PyTorch 2.5.1 CUDA 11.8 build
- TorchAudio 2.5.1
- TorchVision 0.20.1
- Biopython 1.85
- SciPy 1.15.2
- torch-geometric 2.6.1

## Environment Creation

The verified notebook creates the environment with Micromamba:

```text
micromamba -r /content/micromamba_root create   -y -n trRNA2 -f environment.yml
```

Environment verification must confirm CUDA availability before inference.

## Weights

The verified weights archive size was approximately:

```text
0.101 GB
```

The notebook first tries the YangLab download and falls back to the repository-listed Hugging Face mirror if required.

## Optional RNAcentral Database

The initial verification run does not require the optional RNAcentral database because the repository already includes a precomputed example A3M.

For the main benchmark, prefer shared/precomputed A3M files for team reproducibility instead of downloading the ~32 GB database in every Colab session.
