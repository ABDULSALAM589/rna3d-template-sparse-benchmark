# Contribution Workflow

This repository is maintained by the FYP team.

## Branching

Recommended working branches:

- `abdul-models`
- `saniya-benchmark`
- `hamad-evaluation`

Avoid experimental work directly on `main`.

## Typical Workflow

1. Pull the latest `main`.
2. Work on your assigned branch.
3. Keep commits small and descriptive.
4. Push your branch.
5. Open a pull request into `main`.
6. Review major methodological changes before merging.

## Commit Message Examples

- `Add pilot target metadata`
- `Set up DRfold inference environment`
- `Add TM-score evaluation wrapper`
- `Document template-sparsity criterion`
- `Add pilot benchmark results`

## Experiment Changes

Any change that may affect benchmark fairness should be documented, including:

- model version
- preprocessing changes
- sampling budget
- MSA generation method
- secondary-structure source
- template database or cutoff
- evaluation-tool version

## Do Not Commit

Do not commit:

- passwords, API keys, or tokens
- large pretrained weights
- full sequence / structure databases
- large MSA databases
- unnecessary bulk model outputs
