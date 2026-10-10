# RhoFold+ Notes

Verified commit:
`6bdfbda720184409eb682ce08c05d258162ddc48`

Successful Colab run:
```text
Exit code: 0
Runtime: 878.98 s
Peak observed GPU memory: 2659 MiB
GPU: Tesla T4
```

The large runtime is dominated by Amber relaxation:
```text
Neural inference: 15.587 s
Amber relaxation: 852.064 s
```

A non-fatal OpenMM deprecation warning was observed:
`simtk.openmm` is deprecated in favor of `openmm`.

The verification used the bundled precomputed A3M, so the approximately 900 GB automatic-MSA databases were not needed.

Google Drive persistence was verified at:
`/content/drive/MyDrive/RNA3D_Benchmark/RhoFold`

Custom-target cells were prepared but are not claimed as separately verified in the run log supplied for documentation.

Remaining benchmark decisions:
- standardized MSA generation method
- database/version
- MSA depth/quality reporting
- whether relaxation time is reported separately from neural inference time
- failure-handling policy
