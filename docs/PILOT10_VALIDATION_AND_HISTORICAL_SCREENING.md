# Pilot10 validation and historical template-screening workflows

This directory documents five completed, exploratory workflows. Corresponding notebooks live in `notebooks/` and small target-level CSV snapshots in `results/tables/`. All runs use the same ten frozen RNA targets and preserve model outputs and bulky source structures on Google Drive.

| Workflow | Notebook | Committed result |
| --- | --- | --- |
| Independent C3′ RMSD and lDDT-style diagnostics | `pilot10_independent_metric_validation_cpu.ipynb` | `pilot10_independent_metrics.csv` |
| Native-chain/sequence/residue provenance | `pilot10_native_chain_provenance_audit_cpu.ipynb` | `pilot10_native_chain_audit.csv` |
| Initial template/training-overlap evidence inventory | `pilot10_template_scarcity_evidence_inventory_cpu.ipynb` | `pilot10_template_scarcity_evidence_inventory.csv` |
| RCSB release dates and historical RNA sequence candidates | `pilot10_rcsb_historical_sequence_screen_cpu.ipynb` | `pilot10_historical_sequence_screen.csv` |
| Historical structural-template panel, corrected v2 | `pilot10_historical_structural_panel_v2_cpu.ipynb` | `pilot10_historical_structural_panel_v2_summary.csv` |

## Findings and interpretation

- Independent C3′ RMSD cross-checks reproduced archived US-align RMSD to rounding precision across the 30 prediction/native comparisons. Single-atom C3′/C4′ lDDT-style diagnostics are **not** standard all-atom lDDT, and INF was not computed.
- Native-chain provenance: 8 PASS, 2 REVIEW (low experimentally observed residue coverage in `8ubd_H` and `9lq7_K`); 0 FAIL. The check validates the extracted native C3′ coordinates, not all-atom structural correspondence.
- All ten target PDB entries have official initial release dates after 2023-12-31. The RCSB RNA sequence candidate screen found no pre-2024 candidates **at its configured thresholds** (sequence identity 0.3 and E-value 1.0). This is not a proof that homologues or training overlap are absent.
- The structural panel selected 60 candidate RNA entities in release-date/length strata. Of these, 48 were extracted and 480/480 structural alignments scored using a **free structural alignment** (not fixed target residue correspondence). At the panel's screening criteria (native-normalized TM-score ≥0.45 and aligned native coverage ≥0.50), no candidate was flagged. The panel is bounded, non-random, and **not** a comprehensive historical PDB search.
- Exact training structures and release cutoffs for the installed model checkpoints were not independently audited; do not claim template scarcity or absence of train/test contamination on this evidence alone.

## Provenance

Archived read-only results are under `MyDrive/RNA3D_Benchmark/Evaluations/`:

- `pilot10_independent_metric_diagnostics_20261113_v1`
- `pilot10_native_chain_provenance_20261113_v1`
- `pilot10_template_leakage_evidence_inventory_20261113_v1`
- `pilot10_rcsb_release_historical_sequence_candidates_20261113_v1`
- `pilot10_historical_structural_panel_20261114_v2`

The **failed** historical structural panel v1 parsed no structural scores due to a TM-score output regex defect and is intentionally *not* used; the corrected v2 notebook and outputs are recorded here.

## Scope

This commit captures completed validation and screening workflows only. It contains no trRosettaRNA2 pilot10 batch inference, no native structures, no prediction PDBs, no trained weights, and no full-size historical structural score matrix. Native structures were reserved for scoring/audits, not inference-time templates.
