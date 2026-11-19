# RNAbpFlow pilot10 and six-model native-mapped evaluation

## Provenance

RNAbpFlow upstream commit `e8b1c077f7951d4d6ebe00c851d22c37777dfc9f`; checkpoint `RNA3DB.ckpt` SHA-256 `bb598a736193734541f63c59dae75d45db8c04f01a8414a758677367c4b1e213`. Frozen RNA FASTAs plus one **predicted**, non-native IPKnot binary base-pair map per target from the previously frozen NuFold pilot10 input directory. The original model internally replicates a single supplied map into three channels. One deterministic sample `sample_id=0` per target, not native-selected best-of-N. Native coordinates and native BPs were not used for inference.

- `notebooks/rnabpflow_pilot10_ipknot_singlemap_colab.ipynb`: ten-target Colab GPU workflow, recorded per-target output hashes, checkpoints and Drive persistence.
- `notebooks/rnabpflow_pilot10_evaluation_drive_cpu_colab.ipynb`: evaluation Colab workflow.
- `results/tables/rnabpflow_pilot10_scores.csv`: source evaluated per-target results.
- `results/tables/pilot10_six_model_paired.csv`: matched six-model target-level table.
- `results/raw/pilot10_six_model_summary_20261119.json`: reproducible descriptive aggregate.
- External inference records: `MyDrive/RNA3D_Benchmark/RNAbpFlow/runs/rnabpflow_pilot10_ipknot_singlemap_v1`.
- External evaluation records: `MyDrive/RNA3D_Benchmark/RNAbpFlow/Evaluations/rnabpflow_pilot10_ipknot_usalign20260527_20261119_v1` (US-align logs, mapped structures, SHA-256 `FINALIZED.json`, `summary.json`).

## Evaluation protocol

US-align v20260527 (source commit `177cc8a2bbd3e2a6e9c5faaaa4ff5dfa1e6048f7`):

```bash
USalign <mapped_prediction.pdb> <native_eval.pdb> -mol RNA -TMscore 1
```

TM-score normalized to Structure_2 (native). Alignment coverage 1.0 means all experimentally **observed native residues**, not necessarily the complete input chain. RNAbpFlow evaluations completed on the same 10 pilot targets as the earlier five models.

## Exploratory six-model results

| Model | Mean TM-score ↑ | Mean RMSD (Å) ↓ | TM-score target wins |
|---|---:|---:|---:|
| DRfold2 | 0.23449 | 17.59 | 2 |
| NuFold | 0.22284 | 18.34 | 4 |
| RNAbpFlow | 0.21425 | 18.02 | 1 |
| DRfold | 0.19367 | 18.58 | 1 |
| trRosettaRNA2 | 0.19177 | 17.57 | 1 |
| RhoFold+ | 0.18479 | 18.62 | 1 |

RNAbpFlow mean native-normalized TM-score **0.214252**, mean RMSD **18.021 Å**. Results are descriptive and do not establish general model superiority.

## Interpretation limits

This n=10 panel is exploratory, and the six models use different feature and conditioning regimes; RNAbpFlow is explicitly **predicted secondary-structure conditioned** and generated one predetermined sample per RNA. The completeness of native experimental coordinates varies substantially (especially `8ubd_H`, 13/36; `9lq7_K`, 37/49), which affects interpretation. Template scarcity, checkpoint training overlap, and information leakage have not been conclusively cleared. No native-based selection, test-time optimization using reference structures, or claims of statistically significant differences are supported. Bulky PDBs, pretrained weights, and log archives remain on Drive.
