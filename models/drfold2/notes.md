# DRfold2 Setup Notes

## Local Setup Findings

### 1. Arena compiler dependency

The first installer run failed with:

```text
make: clang++: No such file or directory
```

Resolution:

```bash
sudo apt install clang -y
```

After installing Clang, Arena compiled successfully.

### 2. Existing Arena directory

Rerunning `install.sh` produced:

```text
fatal: destination path 'Arena' already exists and is not an empty directory.
```

This was a rerun artifact from the earlier partial installation. Arena compilation itself succeeded afterward.

### 3. Python dependencies

The upstream installer downloaded model weights and built Arena but did not install all Python packages needed for inference.

Observed missing modules included:

```text
numpy
torch
```

The required Python dependencies were installed in the dedicated `drfold2` Conda environment.

### 4. Successful test inference

The model successfully processed the bundled test FASTA and produced:

```text
test_run/relax/model_1.pdb
```

This confirms successful end-to-end inference on the tested local environment.

## Outstanding Reproducibility Work

Before main benchmarking:

- standardize runtime measurement
- standardize peak VRAM measurement
- pin the exact upstream commit used for benchmark runs
- prepare a remote Colab/Kaggle notebook
- prepare a batch inference wrapper
- define the final sampling/output-selection policy
