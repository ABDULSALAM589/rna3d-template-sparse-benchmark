# NuFold Input Specification

For each target:

```text
TARGET/
├── TARGET.fasta
├── TARGET.a3m
└── TARGET.single.ipknot.ss
```

Verified bundled target:

```text
test_input/2DER_C/
├── 2DER_C.fasta
├── 2DER_C.a3m
└── 2DER_C.single.ipknot.ss
```

Primary benchmark rules:
- FASTA from benchmark sequence
- A3M from one standardized MSA pipeline
- SS from one standardized predicted-SS pipeline
- native 3D evaluation-only
- native SS not used in primary inference
