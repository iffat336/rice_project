# Streamlit Deployment Guide

## App Entry Point

```text
app.py
```

Streamlit auto-discovers every file in `pages/` and adds it to the sidebar navigation, so no
extra entry-point configuration is needed beyond pointing the deploy target at `app.py`.

## Required Files

```text
requirements.txt
.streamlit/config.toml
app.py
pages/2_Dataset_Explorer.py
pages/3_Gene_Expression.py
pages/4_Alternative_Splicing.py
pages/5_Machine_Learning.py
pages/6_Candidate_Ranking.py
pages/7_Breeding_Report.py
pages/8_Interview_Notes.py
utils/data_loader.py
utils/analysis.py
utils/ml_model.py
utils/scoring.py
utils/style.py
data/sample_metadata.csv
data/gene_expression.csv
data/splicing_events.csv
data/official_project_candidate_markers.csv
data/thermotolerance_phenotype_demo.csv
```

The remaining `data/*.csv` files (`rice_heat_timecourse_demo.csv`,
`alternative_splicing_events_demo.csv`, `synthetic_rice_heat_stress_candidates.csv`) are only
used by the legacy standalone script `src/rank_candidates.py` and are not required by the
Streamlit dashboard itself.

## Deploy On Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Go to Streamlit Community Cloud.
3. Choose the repository.
4. Set the main file path to:

```text
app.py
```

5. Deploy.

## What To Tell Prof. Calixto

This is an interview prototype called **RiceHeat-AS AI**, not a finished biological analysis. It
shows how I would structure a sub-project under your rice temperature-memory work by integrating:

- A demonstration sample/gene/splicing dataset.
- Differential gene expression (log2 fold change, volcano plot, heatmap).
- Alternative-splicing PSI shifts between control and heat conditions.
- An ML-assisted classifier and feature-importance ranking.
- A combined, weight-adjustable candidate score.
- A breeding-interpretation page and a downloadable candidate report.
- Validation planning through qPCR, RT-PCR, CRISPR, overexpression, or breeding-marker follow-up.
