# RNAbpFlow Notes

## Troubleshooting History

### PyTorch / MKL

Initial error:

```text
ImportError: libtorch_cpu.so: undefined symbol: iJIT_NotifyEvent
```

Resolution:

```text
mkl<2024.1
```

Verified resolved MKL version: 2023.2.0.

### NumPy

NumPy 2.2.6 was incompatible with parts of the PyTorch 2.1.2 environment.

Resolution:

```text
numpy<2
```

Verified working NumPy version: 1.26.4.

### Micromamba ordering

Correct form:

```text
micromamba -r ROOT run -n ENV ...
```

## Successful Verification

```text
Exit code: 0
Total runtime: 60.32 s
Peak observed GPU memory: 641 MiB
GPU: Tesla T4
```

Both bundled example targets completed successfully.

## Scientific Note

RNAbpFlow is explicitly conditioned on base-pair information. Benchmark fairness therefore depends on using the same predicted-BP pipeline for every target in the primary benchmark.

## Remaining Decisions

Before the main benchmark, fix:
- BP-map predictor/source
- number of generated structures per target
- selection/ranking policy for multiple generated structures
- output format used for evaluation
- failure-handling policy
