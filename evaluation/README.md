# Evaluation Pipeline

All feasible models should be evaluated through a common scoring workflow.

## Metrics

### TM-score
Measures global fold similarity.

### RMSD
Measures coordinate deviation after alignment.

### lDDT
Measures local structural accuracy.

### INF
Measures interaction-network fidelity.

### Resource Metrics
Also record runtime and GPU / VRAM usage.

## Principle

Use the same native reference and consistent chain / residue handling across models.

Any metric-specific preprocessing or residue mapping must be documented.
