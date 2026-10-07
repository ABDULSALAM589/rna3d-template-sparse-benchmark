# Experiment Protocol

## Standard Run Record

Every model-target run should record:

- experiment ID
- date
- target ID
- model
- model version / commit
- configuration
- random seed where applicable
- input files
- preprocessing method
- database / template cutoff
- number of generated samples
- selected output rule
- hardware
- runtime
- peak GPU memory
- status
- error notes

## Primary Inference Principle

Use the model's documented inference pipeline while preserving benchmark controls.

Do not use the native experimental target structure as an inference input.

## Model-Specific Inputs

Models may require different information sources, for example:

- sequence
- MSA
- secondary structure
- base-pair maps
- pretrained RNA representations

These differences are not hidden; they are part of the analysis.

## Sampling

For stochastic or multi-sample methods:

- define a fixed sampling budget
- record number of samples
- distinguish first / default prediction from best-of-N analyses
- do not compare an unlimited best-of-N result against a single prediction from another model

## Failed Runs

Do not silently drop failures.

Record:

- model
- target
- failure stage
- error category
- attempted fix
- final status

## Output Naming

Recommended format:

```text
<target_id>__<model>__<config>__seed<seed>__sample<index>.pdb
```

## Result Storage

- raw scores: `results/raw/`
- summary tables: `results/tables/`
- plots: `results/plots/`
- selected structures / visualizations: `results/structures/`
