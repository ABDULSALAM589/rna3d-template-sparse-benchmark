# DRfold input specification

Primary benchmark input:

```text
>target_id
ACGU...
```

Do not supply native PDB/mmCIF coordinates, native secondary structure, native base-pair labels, or template structures. Native 3D is evaluation-only.

DRfold internally generates `seq_ss.npy` using PETfold + ViennaRNA.
