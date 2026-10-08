# DRfold2 Input Specification

## Required Input

### RNA sequence

The documented basic inference command accepts an RNA sequence in FASTA format.

Example:

```fasta
>target_id
AUGCU...
```

## Basic Inference Interface

```bash
python DRfold_infer.py <input.fasta> <output_dir>
```

## Benchmark Input Policy

For primary benchmark runs:

- input sequence must correspond to the selected benchmark RNA target
- the experimental native 3D structure must not be supplied to inference
- no native secondary structure or native base-pair map will be supplied unless a separate oracle experiment is explicitly defined
- any model-generated internal features are treated as part of the model pipeline

## User-Supplied Auxiliary Inputs

For the documented basic inference command, no separate user-supplied file is required for:

- MSA
- secondary structure
- base-pair map
- structural template

This statement describes the official basic command interface and does not imply that the model architecture itself uses no learned evolutionary or structural information.

## Output

Expected final structure:

```text
<output_dir>/relax/model_*.pdb
```
