# Template-Sparsity Definition

## Purpose

This document records the operational definition used to classify RNA targets as template-sparse.

## Important Distinction

**Structural-template scarcity is not the same as evolutionary-information scarcity.**

A target may have no reliable structural template while still having:

- homologous RNA sequences
- a useful MSA
- predictable secondary structure
- base-pair information
- language-model representations

These information sources must be recorded separately.

## Native Structure vs Template

The benchmark target's experimentally solved native structure is used only as evaluation ground truth.

It becomes a leakage risk only if the prediction pipeline can access it, or a sufficiently close structural homolog, during inference.

## Temporal Control

Where practical, use a structural-template/database cutoff that predates the target's experimental release date.

Example:

```text
Template database cutoff: 2024-12-31
Target structure release: 2025-05-10
```

The target native structure is retained privately for scoring but excluded from template access.

## Similarity Control

Template sparsity should not rely only on release date. Close older homologs may still provide strong structural guidance.

The final protocol should therefore record one or more of:

- sequence identity / homology to available structural templates
- structural similarity of candidate templates, where measurable without contaminating inference
- template-search confidence / coverage
- release-date relation to the cutoff

## Thresholds

Exact numerical thresholds should be finalized from literature review and pilot analysis rather than chosen arbitrarily.

The project should document:

- threshold used
- rationale
- sensitivity to alternative thresholds where feasible

## Reporting

Each target should be labeled with:

- cutoff date
- best available template evidence
- sparsity decision
- confidence / notes
