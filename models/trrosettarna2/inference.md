# trRosettaRNA2 Inference

## Basic Command

Verified command:

```bash
python -m trRNA2.predict \
  -i example/seq.a3m \
  -o example/output
```

## Important Options

The verified CLI exposes:

- `-i / --msa`: required A3M MSA
- `-o / --out_dir`: required output directory
- `-ss`: optional custom secondary-structure file
- `-ss_fmt`: `dot_bracket`, `ct`, `bpseq`, or `prob`
- `-nrows`: maximum MSA rows, default 500
- `-nrec`: number of recycles, default 3
- `-relax_steps`: relaxation steps, default 200
- `-gpu`: GPU selection
- `-cpu`: CPU count
- `-pyrosetta`: optional PyRosetta-version behavior
- `-nm`: number of decoys

Without `-ss`, internal `trRNA2-SS` is used.

## Verified Run

```text
Exit code: 0
Runtime: 30.06 s
Peak observed GPU memory: 351 MiB
pLDDT: 0.920
```

Environment:

```text
Python: 3.10.14
NumPy: 2.1.2
PyTorch: 2.5.1
CUDA: True
GPU: Tesla T4
```

## Verified Outputs

```text
example/output/model_1.pdb
example/output/model_1_2D.npz
example/output/model_1_ref200.pdb
example/output/model_1_relaxed200.pdb
example/output/model_1_unrelaxed.pdb
example/output/plddt.csv
```

Primary structure artifact for the verification run:

```text
example/output/model_1_relaxed200.pdb
```

## Benchmark Runs

For each benchmark target:

1. Produce the standardized A3M.
2. Run trRosettaRNA2 with internal SS.
3. Record runtime, GPU and peak VRAM.
4. Store predictions externally if large.
5. Evaluate the chosen output against native coordinates using the common evaluation pipeline.
