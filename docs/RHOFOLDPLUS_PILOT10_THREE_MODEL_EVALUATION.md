# RhoFold+ 10-target pilot and three-model structural evaluation

**Status:** RhoFold+ inference **10/10 complete**; structural evaluation **10/10 scored**, with both NuFold and DRfold2 **10/10 golden calibrations passed**. These are **exploratory pilot** findings, not a final template-sparsity benchmark.

## Reproducible inputs and model conditions

All models were evaluated against the **same ten frozen target IDs** in `configs/rhofoldplus_pilot10_20261111.json`. Their inference-time inputs and output-selection policies were *not* identical:

| Model | Inference condition | Prediction evaluated |
| --- | --- | --- |
| NuFold | Single-record A3M plus predicted IPknot secondary structure | Rank 1 |
| DRfold2 | Default sequence-only FASTA interface | Default single relaxed output |
| RhoFold+ | `--single_seq_pred True`, no searched MSA (depth 1) | `relaxed_1000_model.pdb` |

RhoFold+ is pinned to upstream commit `6bdfbda720184409eb682ce08c05d258162ddc48` and checkpoint SHA-256 `3adb621978dfcd7ea0dc0edeb520d249f423d61530df85ff58a1fad2f33e5608`. Model installation uses the upstream Linux Micromamba environment, with the existing Colab smoke-test command and **1000 Amber relaxation iterations**. The logged per-target runtimes therefore include relaxation rather than only the neural-network forward pass.

**Do not treat this RhoFold+ single-sequence quick-reference mode as its full MSA-based method.** A true MSA-condition benchmark requires harmonized search parameters, database versions, MSA-depth reporting, and a separate run ID.

## Run artifacts and notebooks

- [DRfold2 native-mapped evaluation notebook](../notebooks/drfold2_pilot10_evaluation_colab.ipynb)
- [RhoFold+ resumable pilot/batch Colab notebook](../notebooks/rhofoldplus_pilot10_batch_colab.ipynb)
- [RhoFold+ evaluation and three-model comparison Colab notebook](../notebooks/rhofoldplus_pilot10_evaluation_three_model_colab.ipynb)
- [Frozen RhoFold+ configuration](../configs/rhofoldplus_pilot10_20261111.json)
- [RhoFold+ per-target scores](../results/tables/rhofoldplus_pilot10_structural_scores.csv)
- [Three-model paired scores](../results/tables/pilot10_three_model_paired_scores.csv)
- [NuFold calibration](../results/tables/pilot10_nufold_calibration.csv) / [DRfold2 calibration](../results/tables/pilot10_drfold2_calibration.csv)
- [Immutable evaluation summary](../results/raw/pilot10_three_model_evaluation_summary.json) / [completion checksum manifest](../results/raw/pilot10_three_model_evaluation_finalized.json)
- [RhoFold+ inference records and PDBs on Drive](https://drive.google.com/drive/folders/10wciOg6wEfWC3AlSVtELXVaTV3-_Trkq)
- [Evaluation mapped PDBs and US-align logs on Drive](https://drive.google.com/drive/folders/1sh64qTiXvTE8puzOjHU1lTVpOkzkaj1X)

The notebooks pin the source revisions and include **input validation, read-only integrity checks, explicit pilot/batch gates, completion markers, error-on-incomplete safety, and SHA-256 verification**. Run predictions on GPU; scoring and pairwise comparison run on CPU. Successful targets are skipped without rerunning inference.

## Scoring: matched experimental residues only

To reproduce NuFold's previously established protocol, the evaluation pipeline:
1. Validates each target's input FASTA and existing prediction PDB checksum.
2. Loads the **experimental native PDB** and its per-target position map **only during evaluation**, never inference.
3. Trims the prediction to native-observed target positions, using the same correspondence policy for all three models.
4. Executes **US-align v20260527** with `USalign <mapped_prediction> <native> -mol RNA -TMscore 1`, selecting the TM-score normalized by **Structure_2 = native**.
5. Calibrates against the archived NuFold and DRfold2 scores before scoring RhoFold+ and pairing by target ID.

The 10/10 observed-position alignment coverage must **not** be confused with full-sequence native-coordinate coverage. For example, `8ubd_H` has only **13/36** experimental coordinate positions. Native-coordinate availability is reported separately and an **at least 80%** coverage subset is presented alongside the full ten-target pilot.

## Results (exploratory)

The archived mean values for the **ten paired targets** are:

| Model | Mean native-normalized TM-score ↑ | Median TM-score ↑ | Mean RMSD (Å) ↓ |
| --- | ---: | ---: | ---: |
| NuFold rank 1 | 0.22284 | 0.24423 | 18.337 |
| DRfold2 | 0.23449 | 0.23432 | 17.593 |
| RhoFold+ single sequence | 0.18479 | 0.19321 | 18.622 |

For **eight targets with ≥80% native-coordinate availability**, mean TM-scores were **0.23175 (NuFold), 0.23866 (DRfold2), 0.19382 (RhoFold+)**; mean RMSDs were **16.57, 19.40, 17.70 Å**, respectively.

By the highest *unrounded* per-target TM-score, NuFold led on **5**, DRfold2 on **4**, and RhoFold+ on **1** (`9m31_B`: **0.31046**). These are descriptive counts, **not statistical evidence** of superiority. Several score differences are very small.

## Limitations and follow-up

- **Only ten exploratory targets**; insufficient for conclusive model ranking or claims about template scarcity.
- **Different model input conditions and candidate selection**, and the RhoFold+ reference condition is single-sequence rather than full-MSA.
- **Training-data overlap, template-sparsity screening and release-date leakage controls** still need explicit verification before a publication-level comparison.
- **Incomplete experimental residues** can bias target interpretation; sensitivity analysis by native coordinate fraction is essential.
- lDDT and INF are not computed in this snapshot; RMSD and TM-score must not be mistaken for these metrics.
- The CSVs and provenance JSONs here are **small, checksum-verified snapshots**. Native structures, predicted PDBs, checkpoints, database files and full logs remain in Drive; they have not been uploaded to GitHub.

**Next:** inspect outlier/failure targets and establish template availability / training-overlap controls before expanding to further models.
