# NuFold Notes

Verified commit:
`f77d34af97c1d0f88b47dd2f3c038004fe2ebe13`

Successful run:

```text
Exit code: 0
Runtime: 52.47 s
Peak observed GPU memory: 1231 MiB
GPU: Tesla T4
```

Non-fatal warnings were observed from newer PyTorch/NumPy deprecation behavior. They did not prevent inference.

Important filename correction:
`2DER_C.single.ipknot.ss` is the correct bundled SS file.

Custom target requirement:
`FASTA + A3M + predicted SS`

Remaining benchmark decisions:
- MSA-generation method/database/version
- MSA depth/quality reporting
- predicted-SS settings
- ranked-output selection policy
- failure handling
