# DRfold pilot10 inference, evaluation, and five-model comparison

## Completed scope

Ten fixed pilot RNAs were predicted using **original DRfold** (distinct from DRfold2): `8ubd_H`, `9fia_bJ`, `9cfn_B`, `9m31_B`, `9g4p_B`, `9lq7_K`, `8z8u_B`, `9g6k_lB`, `9cf2_W`, `8wf8_B`.

- DRfold source commit: `9586990c79e4ca488e5f967fcc8bd5b06cd60273`.
- Input: frozen sequence-only FASTA; DRfold internally computes PETfold/ViennaRNA structural features. Native coordinates were **never** used for inference.
- Platforms: Colab T4 (first two targets), Kaggle T4 (other eight). Kaggle checkpoints were captured independently and verified by content hashes. Runtime observations are recorded per target; do not interpret the peak observed VRAM as GPU utilization.
- Output: one `DPR.pdb` per target, with residue counts matching full input length. Bulky predicted PDB files and original inference logs remain on Drive / checkpoint archives, not in Git.

## Evaluation methodology

Evaluation used US-align tag **20260527**, source commit `177cc8a2bbd3e2a6e9c5faaaa4ff5dfa1e6048f7`, with:

```bash
USalign <mapped_drfold_prediction.pdb> <native_eval.pdb> -mol RNA -TMscore 1
```

Reported TM-scores use Structure_2 (native) normalization. Residue mapping restricts comparison to experimentally observed native residues, not the entire sequence if the experimental model is incomplete. All ten DRfold comparisons aligned all available native residues (alignment coverage 1.0). **This does not imply full coordinate coverage of all original target nucleotides**.

Validated immutable evaluation source:
`MyDrive/RNA3D_Benchmark/DRfold/Evaluations/drfold_pilot10_only_usalign20260527_20261119_v1` contains `drfold_scores.csv`, mapped structures, US-align logs, `summary.json`, and SHA-256 inventory `FINALIZED.json`.

Source notebooks and report files:
- `notebooks/drfold_pilot10_first_target_colab.ipynb`: first-target DRfold Colab execution
- `notebooks/drfold_pilot10_kaggle_resume_safe.ipynb`: subsequent target execution + per-target checkpoint ZIP export
- `notebooks/drfold_pilot10_only_evaluation_colab.ipynb`: DRfold-only US-align evaluation in Colab (Drive inputs)
- `results/tables/drfold_pilot10_scores.csv`: original DRfold target-level measurements
- `results/tables/pilot10_five_model_paired.csv`: row-wise join with preceding four-model results
- `results/raw/pilot10_five_model_summary_20261119.json`: deterministic summary and target-win counts

## Descriptive five-model results (n=10)

| Model | Mean native-normalized TM-score ↑ | Mean RMSD (Å) ↓ | Targets with highest TM-score |
|---|---:|---:|---:|
| DRfold2 | 0.23449 | 17.59 | 2 |
| NuFold | 0.22284 | 18.34 | 4 |
| DRfold | 0.19367 | 18.58 | 2 |
| trRosettaRNA2 | 0.19177 | 17.57 | 1 |
| RhoFold+ | 0.18479 | 18.62 | 1 |

DRfold achieved a mean TM-score **0.193667** and mean RMSD **18.583 Å**, winning two of the ten targets by TM-score (`9g6k_lB`, `9cf2_W`). DRfold2 has the highest descriptive mean TM-score in this ten-target panel. These values are **not a statistically established general ranking**.

## Interpretation limits

This exploratory comparison contains only ten RNAs. Models use different input modes and internal feature pipelines. Experimental native coordinate coverage is notably incomplete for `8ubd_H` (13/36) and `9lq7_K` (37/49), making those particular structures harder to interpret. No model checkpoint training-overlap clearance or comprehensive pre-cutoff structural template search has been established. Do not label this cohort definitively template-sparse based solely on current preliminary evidence. All-atom lDDT and INF are not reported here. Preserve input hashes, full scoring logs and checkpoint provenance when expanding the benchmark.
