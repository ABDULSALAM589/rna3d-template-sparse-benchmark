# DRfold inference

Official interface:

```bash
bash DRfold.sh <input.fasta> <output_dir>
```

Primary output:
```text
<output_dir>/DPR.pdb
```

Other outputs include:
- `DPR_0.pdb` ... `DPR_5.pdb`
- `DPRcg.pdb`
- `DPRr1.pdb`
- `geo.npy`
- `geo_1.npy` ... `geo_3.npy`
- `e2e_0.npy` ... `e2e_5.npy`
- `seq_ss.npy`
- `running.log`

Verified bundled run:
- runtime `5669.692 s`
- peak observed GPU memory `1395 MiB`
- final PDB size observed `129.73 KB`
