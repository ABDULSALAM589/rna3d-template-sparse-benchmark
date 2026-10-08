# RNAbpFlow Input Specification

## Required Inputs

RNAbpFlow is not sequence-only. For each target it requires:

1. RNA sequence in FASTA format
2. base-pair conditioning map(s)

Official example layout:

```text
Inputs/TARGET_ID/
├── TARGET_ID.fasta
├── map1.npy
├── map2.npy
└── map3.npy
```

A single `.npy` base-pair map may be replicated three times if only one map is available.

## Target List

Targets are selected through `Inputs/list.txt`.

Example:

```text
TARGET_ID 5
```

## Not Required as External Input

- MSA
- structural template
- native experimental 3D structure

## Benchmark Policy

- FASTA comes from the selected benchmark target.
- BP maps must come from one fixed, documented prediction pipeline.
- Native/ground-truth base pairs must not be used in the primary benchmark.
- Native 3D coordinates are evaluation ground truth only.
- Native-BP experiments must be labelled separately as oracle analyses.
