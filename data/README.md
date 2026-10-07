# Data Directory

This directory stores lightweight benchmark organization files.

## Subdirectories

- `pilot/` — initial 5–10 target pilot set
- `benchmark/` — finalized main benchmark manifests
- `sequences/` — lightweight FASTA files where appropriate
- `metadata/` — target metadata tables and schemas

Large PDB/mmCIF structures and databases should not be committed directly unless explicitly approved and small enough for version control.

## Ground-Truth Policy

Native experimental structures are used for evaluation only and must not be exposed to inference-time template search.
