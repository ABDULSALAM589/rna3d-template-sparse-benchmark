# Benchmark Protocol

## Objective

Construct a controlled benchmark for RNA 3D structure prediction under template-sparse conditions.

## Target Requirements

A target should ideally satisfy all of the following:

1. Experimentally determined native RNA 3D structure is available for evaluation.
2. Target is primarily a single RNA chain within project scope.
3. Structure quality is sufficient for meaningful scoring.
4. Target is non-redundant with other benchmark targets.
5. Structural-template support is limited under the defined cutoff protocol.
6. Training overlap is controlled as far as documented training data and model cutoffs permit.
7. Required model-specific inputs can be generated or obtained consistently.

## Native Structure Policy

The experimental native structure is **ground truth only**.

It must not be supplied to the prediction model or made available as an inference-time template.

## Pilot Benchmark

Use a small pilot subset first to validate:

- preprocessing
- model execution
- output-format consistency
- scoring tools
- runtime and VRAM logging

Target size for the pilot phase: approximately **5–10 RNAs**.

## Main FYP-I Benchmark

The working target range is approximately **30–40 non-redundant template-sparse RNAs**, subject to quality filtering, training-overlap control, model eligibility, and compute feasibility.

This is a planning range, not a fixed guaranteed sample size.

## Fairness Principles

- use the same biological targets across feasible models
- follow documented model input requirements
- report input differences transparently
- use a common scoring pipeline
- use comparable sampling budgets where applicable
- report failed or excluded runs rather than silently removing them
- keep oracle experiments separate from the primary benchmark

## Required Per-Target Records

At minimum:

- target ID
- PDB ID
- chain ID
- RNA sequence
- length
- RNA type where known
- release date
- native structure source
- template cutoff
- template-sparsity status
- training-overlap notes
- MSA information
- secondary-structure / base-pair input source
- per-model eligibility
- notes

## Evaluation

Primary metrics:

- TM-score
- RMSD
- lDDT
- INF
- runtime
- GPU / VRAM usage

Results should be reported both per-target and as aggregate summaries.
