# trRosettaRNA2 Notes

## Verified Repository

```text
Commit: d40a40e36617cb4004a11b0a7603167415ed9c52
```

## Example Layout Observed

```text
example/
├── seq.a3m
├── seq.fasta
├── seq.dbn
├── seq.npz
├── seq.pdb
├── SS/
│   ├── bpseq.bpseq
│   ├── CT.ct
│   ├── dot_bracket.dbn
│   └── prob.txt
└── output/
    ├── model_1.pdb
    ├── model_1_2D.npz
    ├── model_1_ref200.pdb
    ├── model_1_relaxed200.pdb
    ├── model_1_unrelaxed.pdb
    └── plddt.csv
```

## Successful Verification

```text
Exit code: 0
Runtime: 30.06 s
Peak observed GPU memory: 351 MiB
GPU: Tesla T4
pLDDT: 0.920
```

## Important Correction From Initial Notebook Draft

The bundled MSA is:

```text
example/seq.a3m
```

not:

```text
example/msa/seq.a3m
```

The clean notebook uses the correct path.

## Scientific Notes

trRosettaRNA2 uses an A3M MSA and an internal secondary-structure prior by default.

Structural-template scarcity and MSA/evolutionary-information scarcity are distinct. The benchmark should therefore record MSA quality/depth separately from structural-template availability.

## Remaining Decisions

Before main benchmarking, standardize:

- MSA-generation method
- database/version used for MSA search
- MSA depth limits
- whether all targets use default internal SS
- output selection policy
- failure-handling policy
