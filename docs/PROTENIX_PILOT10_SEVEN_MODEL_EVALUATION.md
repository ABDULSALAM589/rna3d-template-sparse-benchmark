# Protenix Pilot10 — corrected inference and seven-model comparison (2026-11-20)

## Validated outcome
- 10/10 frozen RNA sequences: corrected Protenix inference produced finite atomic coordinates, finite essential confidence metrics and SHA-256-verified outputs on Drive.
- Native-residue-mapped US-align v20260527 `USalign mapped_prediction native_eval -mol RNA -TMscore 1`, normalizing by native Structure 2.
- Protenix mean TM-score **0.21175**, mean RMSD **23.214 Å** across ten targets.
- Evaluation source: `MyDrive/RNA3D_Benchmark/Protenix/Evaluations/protenix_pilot10_layernormtorch_usalign20260527_20261120_v1`.
- Inference source: `MyDrive/RNA3D_Benchmark/Protenix/runs/protenix_pilot10_rna_only_nomsa_notemplate_v2_layernormtorch`.

## Reproducibility
- Model `protenix_base_default_v1.0.0`, frozen upstream commit `85767b811c40ed46e73a9b39519cf6bfca8701ba`.
- RNA only, no MSA/RNA-MSA/templates; one sample per target, seed=101, 10 cycles, 200 diffusion steps.
- Tesla T4; fp32, `LAYERNORM_TYPE=torch`, torch triangle multiplication/attention, TF32/cache/fusion disabled.
- **Failed attempt:** initial run generated all-NaN coordinates and confidence scores despite zero CLI errors; not scored. Corrected LayerNorm=torch rerun generated valid coordinates; this is a runtime-configuration recovery, not evidence of a model accuracy improvement.
- Evaluation notebook committed with corrected metadata key `atoms_total` (not `atom_total`).

## Seven-model exploratory comparison

| TM rank | Model | Mean native-normalized TM-score ↑ | Mean RMSD Å ↓ |
|---:|---|---:|---:|
| 1 | DRfold2 | 0.23449 | 17.593 |
| 2 | NuFold | 0.22284 | 18.337 |
| 3 | RNAbpFlow | 0.21425 | 18.021 |
| 4 | Protenix | 0.21175 | 23.214 |
| 5 | DRfold | 0.19367 | 18.583 |
| 6 | trRosettaRNA2 | 0.19177 | 17.571 |
| 7 | RhoFold+ | 0.18479 | 18.622 |

## Methodological boundaries
- Pilot is n=10 only; scores do **not** establish general model superiority or statistically robust differences.
- Inputs are not equally conditioned across models (including RNAbpFlow with predicted IPKnot secondary-structure map).
- Experimental native structures can have missing coordinates; mapping retains only observed native residues, e.g., 8ubd_H has 13/36 observed.
- Template scarcity and training-set overlap have not yet been independently validated.
- All large structures, raw logs, checkpoints and full evaluation artifacts remain on Google Drive; repository contains notebooks and small summary/score tables.

## Repository files
- `notebooks/protenix_pilot10_fullbatch_layernormtorch_colab.ipynb`: GPU batch inference and strict geometry verification.
- `notebooks/protenix_pilot10_usalign_native_mapped_cpu_colab.ipynb`: CPU evaluation using native-mapped US-align (metadata typo fixed).
- `results/tables/protenix_pilot10_scores.csv`: full per-target metrics.
- `results/tables/pilot10_seven_model_paired.csv`: expanded paired comparison.
- `results/raw/pilot10_seven_model_summary_20261120.json`: seven-model aggregate.
