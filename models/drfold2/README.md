# DRfold2

## Status

**READY — successful end-to-end local inference verified.**

DRfold2 is one of the candidate RNA 3D structure prediction methods in this benchmark.

## Upstream

- **Official repository:** https://github.com/leeyang/DRfold2
- **Method:** DRfold2 — ab initio RNA structure prediction with a composite language model and denoised end-to-end learning
- **Upstream main commit observed during setup:** `3667d6ac44c5b14cff94c36e0371224acb2cdae5`
- **License:** MIT-style license in the upstream repository

## Local Verification

The model was successfully installed and tested on the local workstation.

- **Operating system:** Ubuntu 26.04
- **Conda environment:** `drfold2`
- **Python:** 3.10.22
- **PyTorch:** 2.14.1+cu130
- **CUDA available:** Yes
- **GPU:** NVIDIA GeForce RTX 5070
- **NumPy:** 2.2.6
- **SciPy:** 1.15.3

## Input

The documented basic inference interface requires:

- RNA sequence in FASTA format
- output directory

No separate MSA, secondary-structure, base-pair, or template file is supplied in the documented basic inference command.

## Inference

```bash
python DRfold_infer.py <input.fasta> <output_dir>
```

Verified local test:

```bash
python DRfold_infer.py test/seq.fasta test_run
```

## Output

The final relaxed prediction is written under:

```text
<output_dir>/relax/model_*.pdb
```

Verified output:

```text
test_run/relax/model_1.pdb
```

The run also generated multiple intermediate candidate structures under `rets_dir/` and `folds/`.

## Benchmark Use

For the final benchmark:

1. Use the benchmark RNA sequence as FASTA input.
2. Do not provide the experimental native 3D structure to the model.
3. Save the predicted structure using a standardized target/model naming convention.
4. Record runtime, GPU, peak VRAM, model commit, and configuration.
5. Evaluate the prediction against the native structure only after inference.

## Current Readiness

- [x] Official repository verified
- [x] Environment created
- [x] Model weights downloaded
- [x] Arena compiled
- [x] GPU detected
- [x] Test FASTA processed
- [x] Predicted PDB generated
- [x] Final relaxed structure generated
- [ ] Runtime benchmarking standardized
- [ ] Peak VRAM logging standardized
- [ ] Colab/Kaggle notebook prepared
- [ ] Batch benchmark wrapper prepared
