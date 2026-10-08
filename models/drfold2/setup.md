# DRfold2 Setup

## Tested Local Environment

```text
OS: Ubuntu 26.04
Conda environment: drfold2
Python: 3.10.22
PyTorch: 2.14.1+cu130
NumPy: 2.2.6
SciPy: 1.15.3
GPU: NVIDIA GeForce RTX 5070
CUDA available: True
```

## Environment Creation

```bash
conda create -n drfold2 python=3.10 -y
conda activate drfold2
```

## Clone

```bash
git clone https://github.com/leeyang/DRfold2.git
cd DRfold2
```

## Upstream Installer

```bash
bash install.sh
```

The upstream installer downloads approximately 1.3 GB of model weights and clones/builds Arena.

### Important setup observation

The upstream `install.sh` does not install all Python dependencies. During local setup, the Python environment required manual installation of packages including PyTorch, NumPy, and SciPy.

Arena compilation also required `clang++` on the tested Ubuntu system.

```bash
sudo apt update
sudo apt install clang -y
```

Then the installer/build was rerun successfully.

## Verification

```bash
python - <<'PY'
import torch, numpy, scipy
print("Torch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
print("NumPy:", numpy.__version__)
print("SciPy:", scipy.__version__)
PY
```

Verified output included:

```text
CUDA available: True
GPU: NVIDIA GeForce RTX 5070
```

## Storage Note

Model weights and large caches are not stored in this benchmark repository. The local DRfold2 installation is used for development/testing; remote execution will be documented separately for reproducible benchmark runs.
