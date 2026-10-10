# RhoFold+ Input Specification

## Primary Benchmark Input
```text
TARGET.fasta
TARGET.a3m
```

Verified example:
```text
example/input/3owzA/3owzA.fasta
example/input/3owzA/3owzA.a3m
```

For the primary FYP benchmark:
- FASTA comes from the benchmark target sequence
- A3M comes from one standardized MSA-generation policy
- native 3D structure is evaluation-only
- record MSA depth/quality separately from structural-template availability

## Sequence-Only Mode
RhoFold+ also supports `--single_seq_pred True`, but upstream documentation describes this as a testing/quick-reference mode and less accurate than MSA-based prediction.

It must therefore be reported separately from the primary benchmark.
