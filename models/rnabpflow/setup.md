# RNAbpFlow Setup

## Verified Environment

```text
Platform: Google Colab
Python: 3.10
NumPy: 1.26.4
PyTorch: 2.1.2
CUDA available: True
GPU: Tesla T4
RNAbpFlow commit: e8b1c077f7951d4d6ebe00c851d22c37777dfc9f
Checkpoint: RNA3DB.ckpt
```

## Official Environment

The upstream repository provides `RNAbpFlow.yml`, which pins Python 3.10, PyTorch 2.1.2 and CUDA 11.8.

## Colab Compatibility Fixes

The verified Colab runtime required:

```bash
micromamba -r /content/micromamba_root install \
  -n RNAbpFlow -y -c conda-forge \
  "mkl<2024.1" \
  "numpy<2"
```

### MKL issue

Initial PyTorch import failed with:

```text
ImportError: libtorch_cpu.so: undefined symbol: iJIT_NotifyEvent
```

The working environment resolved to MKL 2023.2.0.

### NumPy issue

NumPy 2.2.6 produced compatibility warnings with PyTorch 2.1.2. Pinning `numpy<2` produced NumPy 1.26.4.

## Correct Micromamba Invocation

Use:

```text
micromamba -r ROOT run -n ENV ...
```
