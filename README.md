# RNA 3D Structure Prediction for Template-Sparse RNA Sequences

A research and development FYP focused on controlled benchmarking of RNA 3D structure prediction methods under template-sparse conditions.

## Project Goal

The project studies which RNA 3D structure prediction strategies remain reliable when a target RNA has limited structural-template support. The work emphasizes a common, reproducible benchmark, transparent input conditions, multi-metric evaluation, and analysis of factors that influence success or failure.

## Research Question

> Which RNA 3D prediction strategies remain more reliable under controlled template-sparse conditions, and what factors influence their success or failure?

## Repository Role

This repository is the **source of truth for code, benchmark metadata, experiment definitions, configurations, environment files, documentation, evaluation scripts, and small result artifacts**.

Large model weights, sequence/MSA databases, native-structure collections, cached model features, and bulk prediction outputs are stored externally (for example, Hugging Face or Google Drive) and are not version-controlled here.

## Repository Structure

```text
.
├── data/           # metadata, FASTA sequences, manifests, lightweight benchmark files
├── models/         # per-model setup and inference documentation
├── scripts/        # preprocessing, inference, and utility scripts
├── evaluation/     # TM-score, RMSD, lDDT, INF workflows
├── configs/        # experiment and model configurations
├── environments/   # Conda/requirements files and setup notes
├── results/        # small CSVs, summary tables, plots, selected artifacts
├── docs/           # benchmark protocol and methodology documentation
└── notebooks/      # Colab/Kaggle notebooks
```

## Compute & Storage Architecture

```text
GitHub
  ├── code
  ├── configs
  ├── metadata
  ├── notebooks
  ├── documentation
  └── small results

External storage (Hugging Face / Google Drive)
  ├── model weights
  ├── native structures
  ├── MSA files
  ├── secondary-structure / base-pair features
  ├── large prediction outputs
  └── large databases

Compute
  ├── local GPU
  ├── Google Colab
  └── Kaggle
```

## Candidate Methods

- RhoFold+
- NuFold
- DRfold
- DRfold2
- trRosettaRNA2
- RNAbpFlow
- Protenix

Final inclusion in the full benchmark depends on reproducibility, code availability, compatibility with benchmark targets, and computational feasibility.

## NuFold 10-Target Pilot

The resume-safe batch inference, evaluation, and Colab launcher are documented in [`models/nufold/pilot_batch.md`](models/nufold/pilot_batch.md). The pipeline reads only the externally supplied frozen pilot manifest (kept out of the automation commit as dataset content), writes artifacts to a run-ID directory, labels single-sequence A3M baselines separately from genuine MSAs, and keeps native coordinates out of inference inputs.

## Three-model exploratory pilot (November 2026)

NuFold, DRfold2, and **RhoFold+ (single-sequence quick-reference condition)** have **10/10 completed predictions and native-mapped structural scores** on the same pilot targets. The RhoFold+ evaluation also reproduces both earlier models' scores (10/10 calibrations each). For provenance, scored CSV snapshots and caveats see [the three-model pilot report](docs/RHOFOLDPLUS_PILOT10_THREE_MODEL_EVALUATION.md). This is **not** a finalized full-MSA or template-sparsity comparison.

## Five-model exploratory pilot (November 2026)

**NuFold, DRfold2, RhoFold+, trRosettaRNA2, and original DRfold** now have 10/10 predictions and native-mapped structural evaluations on the frozen pilot targets. trRosettaRNA2 used single-sequence A3Ms (depth 1); the four-model comparison is exploratory because input modes and native coordinate availability differ. See [the DRfold five-model evaluation report](docs/DRFOLD_PILOT10_FIVE_MODEL_EVALUATION.md), [the trRosettaRNA2 pilot report](docs/TRROSETTARNA2_PILOT10.md), and committed per-target score CSVs. **No template-sparsity or training-overlap clearance is inferred.**

## Six-model exploratory pilot (November 2026)

**RNAbpFlow** completed 10/10 predicted-IPKnot-conditioned, single-sample predictions and native-mapped evaluations, completing six models × ten RNA targets. See [the RNAbpFlow six-model report](docs/RNABPFLOW_PILOT10_SIX_MODEL_EVALUATION.md) and [six-model paired CSV](results/tables/pilot10_six_model_paired.csv). The exploratory panel is **not** a controlled identical-input or leakage-cleared benchmark.

## Benchmark Principles

1. Experimental native 3D structures are used as evaluation ground truth only.
2. Native target structures must not be exposed as inference-time templates.
3. Template availability is controlled using documented cutoffs and similarity checks.
4. Training-data overlap is controlled as far as documented training data and model cutoffs permit.
5. The same biological targets are used across feasible models.
6. Model-specific inputs such as MSA, secondary structure, and base-pair information are recorded explicitly.
7. Predictions are scored through a common evaluation pipeline.

## Evaluation Metrics

- TM-score
- RMSD
- lDDT
- INF
- runtime
- GPU / VRAM usage

## FYP-I Focus

- benchmark target collection and metadata curation
- template-sparsity characterization
- model setup and pilot execution
- model-specific preprocessing
- standardized evaluation
- controlled benchmarking
- factor and failure analysis
- reproducible experiment records

## Team

- Abdul Salam Kalhoro
- Saniya
- Hamadullah

## Status

**FYP-I exploratory execution phase — six models scored on ten pilot targets; template-sparsity controls, expanded cohort, and full-MSA conditions remain pending.**


## Protenix Pilot10 and seven-model evaluation (2026-11-20)

Protenix corrected RNA-only single-sequence inference passed 10/10 finite-coordinate checks, then native-mapped US-align v20260527 evaluation scored all ten targets (mean TM-score **0.21175**, mean RMSD **23.214 Å**). The original default-layernorm attempt generated invalid NaN geometry; valid results require `LAYERNORM_TYPE=torch` with conservative fp32/T4 settings. See [Protenix seven-model evaluation](docs/PROTENIX_PILOT10_SEVEN_MODEL_EVALUATION.md). Results are exploratory, input conditioning differs, and template scarcity/leakage checks remain pending.
