# NuFold Inference

Verified command:

```bash
python run_nufold.py \
  --ckpt_path checkpoints/global_step145245.pt \
  --input_fasta test_input/2DER_C/2DER_C.fasta \
  --input_dir test_input/ \
  --output_dir test_output \
  --config_preset initial_training
```

Verified result:

```text
Exit code: 0
Runtime: 52.47 s
Peak observed GPU memory: 1231 MiB
```

Generated files included:
- `2DER_C_rank_1.pdb` through `2DER_C_rank_5.pdb`
- `2DER_C_plddt_plot.png`
- `2DER_C_in_0.pkl`
- `2DER_C_out_0.pkl`

Primary verification artifact:
`2DER_C_rank_1.pdb`

The finalized notebook also contains a custom-target workflow that creates FASTA, predicts SS with IPknot, accepts an uploaded A3M, runs inference, verifies ranked PDBs, logs runtime/VRAM, and optionally saves to Drive.
