# RNA 3D Structure Prediction for Template-Sparse RNA Sequences

A research and development FYP focused on **controlled benchmarking of RNA 3D structure prediction methods under template-sparse conditions**.

## Project Goal

The project studies which RNA 3D structure prediction strategies remain reliable when a target RNA has limited structural-template support. The work emphasizes a **common, reproducible benchmark**, transparent input conditions, multi-metric evaluation, and analysis of factors that influence success or failure.

## Research Question

> Which RNA 3D prediction strategies remain more reliable under controlled template-sparse conditions, and what factors influence their success or failure?

## FYP-I Focus

FYP-I concentrates on:

- literature review and method finalization
- benchmark target collection and metadata curation
- definition and characterization of template sparsity
- model environment setup
- model-specific preprocessing pipelines
- standardized evaluation and resource logging
- pilot execution
- controlled benchmarking
- factor and failure analysis
- reproducible experiment records and reporting

FYP-II will use FYP-I evidence to select a promising, accurate, and computationally feasible candidate for extended benchmarking, optimization, ablation, and validation.

## Candidate Methods

The initial candidate set includes:

- RhoFold+
- NuFold
- DRfold
- DRfold2
- trRosettaRNA2
- RNAbpFlow
- Protenix

Final inclusion in the full benchmark depends on code availability, reproducibility, compatibility with the benchmark targets, and computational feasibility.

## Benchmark Philosophy

The benchmark is intended to use **experimentally solved RNA structures as ground truth for evaluation**, while preventing those native structures from becoming inference-time templates.

Key principles:

1. Native experimental 3D structures are used only for evaluation.
2. Template availability is controlled using documented cutoffs and similarity checks.
3. Training-data overlap is controlled as far as documented model training data and cutoffs permit.
4. The same biological targets are used across feasible models.
5. Each model is run with its documented input requirements.
6. Model-specific inputs such as MSA, secondary structure, or base-pair information are recorded explicitly.
7. All predictions are scored using a common evaluation pipeline.

## Primary Evaluation Metrics

- **TM-score** — global fold similarity
- **RMSD** — coordinate deviation
- **lDDT** — local structural accuracy
- **INF** — interaction network fidelity
- **Runtime**
- **GPU / VRAM usage**

No single metric is treated as the sole definition of a winning model.

## Repository Structure

```text
.
├── README.md
├── CONTRIBUTING.md
├── .gitignore
├── docs/
├── data/
│   ├── pilot/
│   ├── benchmark/
│   ├── sequences/
│   └── metadata/
├── models/
├── scripts/
│   ├── preprocessing/
│   ├── inference/
│   └── utilities/
├── evaluation/
├── predictions/
├── results/
│   ├── raw/
│   ├── tables/
│   ├── plots/
│   └── structures/
├── configs/
├── logs/
└── environments/
```

## Team

- Abdul Salam Kalhoro
- Saniya
- Hamadullah

## Reproducibility Rules

For every benchmark run, record:

- target ID and chain
- model name and version / commit
- configuration
- input files and input-generation method
- database or template cutoff where applicable
- random seed where applicable
- hardware
- runtime
- peak GPU memory where available
- output structure path
- evaluation scores
- warnings, failures, or deviations from the standard protocol

## Data Policy

Large structural databases, pretrained weights, MSA databases, checkpoints, and bulk generated predictions should **not** be committed directly to GitHub. Store lightweight metadata, scripts, configs, and small reproducibility artifacts in the repository, and document how larger resources are obtained.

## Status

**FYP-I execution phase — benchmark foundation and pilot setup.**
