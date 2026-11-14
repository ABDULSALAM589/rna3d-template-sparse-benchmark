# trRosettaRNA2 Pilot10 — Inference and Four-Model Structural Evaluation

**Status:** 10/10 inference PASS; 10/10 native-mapped US-align evaluations complete.

## Reproduce / inspect

- Inference notebook: `notebooks/trrosettarna2_pilot10_batch_colab.ipynb` (Colab GPU)
- Evaluation notebook: `notebooks/trrosettarna2_pilot10_evaluation_colab.ipynb` (Colab CPU)
- Frozen configuration: `configs/trrosettarna2_pilot10_20261114.json`
- Inference summary: `results/tables/trrosettarna2_pilot10_inference.csv`
- Target-level trRosettaRNA2 scores: `results/tables/trrosettarna2_pilot10_scores.csv`
- Paired NuFold × DRfold2 × RhoFold+ × trRosettaRNA2 results: `results/tables/pilot10_four_model_paired.csv`

### Experimental conditions

The ten frozen target IDs are `8ubd_H, 9fia_bJ, 9cfn_B, 9m31_B, 9g4p_B, 9lq7_K, 8z8u_B, 9g6k_lB, 9cf2_W, 8wf8_B`.
trRosettaRNA2 source is pinned to `d40a40e36617cb4004a11b0a7603167415ed9c52`.
Each target used exactly **one A3M sequence** (MSA depth 1), sourced from the frozen NuFold input snapshot. The chosen prediction was `model_1_relaxed200.pdb`; model output and all original inference logs remain on Google Drive. **No native target coordinates were provided as inference input.**

The CPU evaluation uses native experimentally observed residue positions (mapped from the frozen residue maps) and US-align tag `20260527`, with `-mol RNA -TMscore 1`. Scores are normalized by the second structure (native). Original full-length predictions were not modified: mapped PDBs exist as separate evaluation artifacts.

### Mean results (n=10)

| Method | Mean native-normalized TM-score ↑ | Mean RMSD (Å) ↓ |
|---|---:|---:|
| NuFold (rank 1) | 0.222836 | 18.337 |
| DRfold2 | 0.234494 | 17.593 |
| RhoFold+ (single-sequence quick-reference) | 0.184790 | 18.622 |
| **trRosettaRNA2 (single-sequence A3M)** | **0.191773** | **17.571** |

All ten trRosettaRNA2 predictions passed sequence and residue-count checks. Native-observed-position alignment coverage was 1.0 for every target. **This does not mean all original native structures have 100% coordinate coverage**: two targets have particularly incomplete experimentally observed native residues and are tracked separately.

### Immutable source results

- Inference: `MyDrive/RNA3D_Benchmark/trRosettaRNA2/runs/trrosettarna2_pilot10_single_20261114_v1`
- Evaluation: `MyDrive/RNA3D_Benchmark/Evaluations/trrosettarna2_pilot10_fourmodel_eval_20261115_v1`
- Evaluation archive includes `FINALIZED.json` with SHA-256 hashes of score CSVs, mapped PDBs and US-align logs. Inspect archive before attempting any rerun; never overwrite completed runs.

**Limitations:** exploratory sample of 10 RNAs; different model preprocessing and prediction selection; some experimental native residues absent; training-overlap and historical template scarcity are not established; TM-score interpretation is especially sensitive for short RNAs. No statistically supported general model ranking is claimed.
