# DRfold2 Inference

## Single-Target Prediction

Activate the environment:

```bash
conda activate drfold2
cd ~/FYP/models/DRfold2
```

Run:

```bash
python DRfold_infer.py <input.fasta> <output_dir>
```

Verified test command:

```bash
python DRfold_infer.py test/seq.fasta test_run
```

## Verified Output

The successful local run generated:

```text
test_run/relax/model_1.pdb
```

It also generated intermediate candidate structures in:

```text
test_run/rets_dir/
test_run/folds/
```

## Multi-Model Option

The upstream README documents an optional third argument for multiple model prediction:

```bash
python DRfold_infer.py <input.fasta> <output_dir> 1
```

The exact sampling policy used for the final benchmark must be fixed before large-scale runs so that comparisons remain fair across models.

## Planned Benchmark Wrapper

A later batch script will:

1. iterate over benchmark FASTA files
2. create one output directory per target
3. run DRfold2
4. capture runtime and exit status
5. record GPU/VRAM statistics
6. locate the final relaxed PDB
7. write a standardized result manifest

The batch wrapper is not yet implemented.
