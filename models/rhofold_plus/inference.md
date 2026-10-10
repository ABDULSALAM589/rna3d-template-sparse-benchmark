# RhoFold+ Inference

## Verified Command
```bash
python inference.py \
  --input_fas ./example/input/3owzA/3owzA.fasta \
  --input_a3m ./example/input/3owzA/3owzA.a3m \
  --output_dir ./example/output/3owzA_verify \
  --ckpt ./pretrained/RhoFold_pretrained.pt \
  --device cuda:0
```

## Verified Result
```text
Exit code: 0
Total runtime: 878.98 s
Peak observed GPU memory: 2659 MiB
```

The log separated this into:
```text
RhoFold Inference: 15.587 s
Amber Relaxation 1000 iterations: 852.064 s
```

## Verified Outputs
```text
log.txt
results.npz
ss.ct
unrelaxed_model.pdb
relaxed_1000_model.pdb
```

Primary verification artifact:
`relaxed_1000_model.pdb`

## Custom Target
The notebook contains:
1. custom FASTA + uploaded/precomputed A3M mode — recommended
2. custom sequence-only mode — ablation/quick reference only
