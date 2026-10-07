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

**FYP-I execution phase — benchmark foundation, model setup, and pilot preparation.**
