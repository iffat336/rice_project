# RiceHeat-AS AI Dashboard

AI-Assisted Gene and Splicing Marker Discovery for Heat-Tolerant Rice. A deployable Streamlit
interview demo for Prof. Dr. Cristiane Paula Gomes Calixto's FAPESP research area.

## Project Title

RiceHeat-AS AI: An Explainable Machine-Learning Dashboard for Identifying Gene Expression and
Alternative-Splicing Markers of Heat-Stress Tolerance in Rice

## Why This Fits The Lab

Prof. Calixto's major project is "Transcriptome-wide analysis of rice temperature memory and heat
responses" (FAPESP Young Investigator Grant 19/13158-8, 2021-2027, IB-USP). It focuses on rice heat
stress, basal and acquired thermotolerance, gene expression, alternative splicing, and candidate
validation through CRISPR-Cas9 or overexpression.

This dashboard is a computational prototype, not a wet-lab project. It does not replace biological
validation; it uses machine learning and structured scoring to prioritize a small set of genes and
splicing events that deserve deeper experimental follow-up.

## Core Research Question

Can transcriptomic and alternative-splicing data be used to identify candidate genes associated with
rice heat-stress tolerance and prioritize them for future breeding or functional validation?

## Folder Structure

```text
rice-heat-stress-ai/
  app.py                          # Project Overview (entry point)
  requirements.txt
  .streamlit/
    config.toml
  pages/
    2_Dataset_Explorer.py
    3_Gene_Expression.py
    4_Alternative_Splicing.py
    5_Machine_Learning.py
    6_Candidate_Ranking.py
    7_Breeding_Report.py
    8_Interview_Notes.py
  utils/
    data_loader.py                # cached CSV loaders
    analysis.py                   # differential expression / reshaping
    ml_model.py                   # feature matrix + Random Forest classifier
    scoring.py                    # weighted candidate scoring
    style.py                      # shared CSS and metric cards
  data/
    sample_metadata.csv
    gene_expression.csv
    splicing_events.csv
    official_project_candidate_markers.csv
    thermotolerance_phenotype_demo.csv
    rice_heat_timecourse_demo.csv         (legacy, used by src/rank_candidates.py)
    alternative_splicing_events_demo.csv  (legacy, used by src/rank_candidates.py)
    synthetic_rice_heat_stress_candidates.csv (legacy)
  src/
    rank_candidates.py            # standalone CLI ranking script (legacy demo)
  web/
    index.html, styles.css, app.js  # static HTML backup demo
  docs/
    interview_script.md, methods_plan.md, professor_profile.md,
    research_sources.md, streamlit_deploy.md
```

## Dashboard Pages

1. **Project Overview** - research problem, hypothesis, and pipeline summary.
2. **Dataset Explorer** - sample metadata, gene panel, splicing panel, and filters.
3. **Gene Expression** - top heat-responsive genes, log2 fold change, volcano plot, heatmap.
4. **Alternative Splicing** - PSI shift (Percent Spliced In) between control and heat conditions.
5. **Machine Learning** - Random Forest classifier (Control vs Heat or Tolerant vs Sensitive), ROC curve, feature importance.
6. **Candidate Ranking** - combined, weight-adjustable candidate score table.
7. **Breeding Report** - breeding-value interpretation, phenotype chart, downloadable report.
8. **Interview & Validation** - professor profile, validation routes, and the interview pitch script.

## Run The Streamlit App

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run The Legacy Candidate Ranking Script

No external Python packages are required.

```bash
python src/rank_candidates.py --focus balanced
python src/rank_candidates.py --focus splicing
python src/rank_candidates.py --focus memory
python src/rank_candidates.py --focus breeding
```

## Open The Static HTML Demo

Open this file in a browser:

```text
web/index.html
```

The Streamlit dashboard is the main demo for deployment. The static HTML demo remains as a backup.

## Important Note

The data in this project is synthetic demonstration data built around real heat-stress candidate
genes reported in rice transcriptome studies (e.g. OsHSP70, OsHSFA2d, OsHDAC6, OsSR45, OsTRBF1). It
is created to explain the analysis workflow during an interview. Real research would require public
RNA-seq reanalysis (e.g. SRP190858), lab-generated rice stress samples, or both.
