# DRfold notes

The verified upstream bundled target was `77 nt`.

The successful run emitted non-fatal warnings:
- PyTorch checkpoint warnings about `requires_grad`
- L-BFGS line-search warnings
- deprecated `simtk.openmm` import warning
- `pkg_resources` deprecation warning

These did not prevent completion: exit code was `0` and `DPR.pdb` was generated.

For the benchmark, DRfold is treated as sequence → internally predicted SS/features → 3D. Keep it separate from DRfold2.

Custom-target cells are included in the cleaned notebook, but the verified evidence recorded here is from the official bundled test target.
