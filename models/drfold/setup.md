# DRfold setup

Verified stack:
- Python `3.9.19`
- NumPy `1.23.5`
- SciPy `1.13.1`
- PyTorch `1.13.1+cu117`
- OpenMM `7.7`
- ViennaRNA `2.4.18`
- PETfold `2.0`
- Micromamba `2.9.0`
- Tesla T4

PETfold compatibility fixes required:
- current ViennaRNA include/library paths
- `-fcommon`
- `-lstdc++`
- build `../bin/PETfold` directly
- wrapper that runs from the directory containing `scfg.rate`
