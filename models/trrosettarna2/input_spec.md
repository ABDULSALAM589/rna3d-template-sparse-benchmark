# trRosettaRNA2 Input Specification

## Required Input

The standalone prediction interface requires an RNA MSA in A3M format:

```text
python -m trRNA2.predict -i TARGET.a3m -o OUTPUT_DIR
```

Verified example:

```text
example/seq.a3m
```

## Optional Secondary Structure

The prediction interface supports:

```text
-ss SS_FILE
-ss_fmt {dot_bracket,ct,bpseq,prob}
```

If no custom SS is provided, trRosettaRNA2 uses its internal `trRNA2-SS` predictor.

Bundled example SS formats include:

```text
example/SS/bpseq.bpseq
example/SS/CT.ct
example/SS/dot_bracket.dbn
example/SS/prob.txt
```

## Not Used as Primary Inference Input

- native experimental 3D structure
- structural template coordinates

## Benchmark Policy

For the primary benchmark:

- generate one target-specific A3M per benchmark RNA
- use one standardized MSA-generation policy across all targets
- use internal `trRNA2-SS`
- keep native 3D coordinates evaluation-only

Custom predicted SS can be evaluated as a separate ablation. Native SS, if used at all, must be reported as an oracle condition and never mixed with primary results.
