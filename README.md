# RiceHeat-AS AI Dashboard

**AI-Assisted Gene and Splicing Marker Discovery for Heat-Tolerant Rice**

A deployable Streamlit prototype built for a PhD interview with Prof. Dr. Cristiane Paula Gomes
Calixto (Institute of Biosciences, University of Sao Paulo). It integrates gene-expression data,
alternative-splicing indicators, and machine learning to prioritize rice genes for heat-stress
tolerance research and climate-resilient breeding.

> This is a computational prototype, not a wet-lab result. All numbers come from a small synthetic
> demonstration dataset built around real candidate genes reported in rice heat-stress literature.
> It exists to explain a research workflow, not to claim original biological findings.

---

## Table of Contents

1. [Project Title](#project-title)
2. [Why This Fits The Lab](#why-this-fits-the-lab)
3. [Core Research Question](#core-research-question)
4. [Main Hypothesis](#main-hypothesis)
5. [Project Objectives](#project-objectives)
6. [How This Differs From The Official FAPESP Project](#how-this-differs-from-the-official-fapesp-project)
7. [Dataset](#dataset)
8. [Methods Workflow](#methods-workflow)
9. [Candidate Scoring Formula](#candidate-scoring-formula)
10. [Dashboard Pages](#dashboard-pages)
11. [Folder Structure](#folder-structure)
12. [Tech Stack](#tech-stack)
13. [Running The Project](#running-the-project)
14. [Deployment](#deployment)
15. [Limitations](#limitations)
16. [Future Work](#future-work)

---

## Project Title

**RiceHeat-AS AI: An Explainable Machine-Learning Dashboard for Identifying Gene Expression and
Alternative-Splicing Markers of Heat-Stress Tolerance in Rice**

## Why This Fits The Lab

Prof. Calixto's major project is *"Transcriptome-wide analysis of rice temperature memory and heat
responses"* (FAPESP Young Investigator Grant 19/13158-8, June 2021 - May 2027, IB-USP). It studies
rice cultivars contrasting for thermotolerance, basal and acquired thermotolerance, gene expression
and alternative splicing under heat stress, and validates candidate regulators through CRISPR-Cas9
and overexpression lines.

RiceHeat-AS AI does not copy that wet-lab project. It proposes the computational layer that could
sit alongside it: a transparent workflow that takes transcriptomic and splicing signals and turns
them into a ranked, explainable shortlist of candidates for the lab to validate.

## Core Research Question

Can transcriptomic and alternative-splicing data be used to identify candidate genes associated
with rice heat-stress tolerance and prioritize them for future breeding or functional validation?

## Main Hypothesis

Rice heat-stress tolerance is controlled not only by changes in gene-expression levels but also by
post-transcriptional regulation such as alternative splicing. Integrating differential expression,
alternative-splicing indicators, and machine-learning feature ranking can help prioritize candidate
genes for future validation and climate-resilient rice breeding.

## Project Objectives

1. Analyze rice heat-stress gene-expression data and identify genes responsive to high temperature.
2. Detect genes showing strong alternative-splicing changes under heat stress.
3. Apply machine-learning models to classify heat-stress response and rank important genes.
4. Integrate expression, splicing, and ML outputs into a single candidate-gene scoring system.
5. Translate the computational output into breeding-focused recommendations through an interactive
   Streamlit dashboard.

## How This Differs From The Official FAPESP Project

| Prof. Calixto's official project | This prototype |
| --- | --- |
| Wet-lab, transcriptome-wide rice heat-stress study | Computational prototype and dashboard |
| Studies temperature memory, basal/acquired thermotolerance | Explainable AI workflow for candidate prioritization |
| Uses RNA-seq, alternative-splicing analysis, CRISPR/overexpression validation | Uses demo expression data, splicing indicators, ML, and visualization |
| Generates original biological knowledge | Converts biological knowledge into a decision-support tool |

## Dataset

All data lives in `data/` and is synthetic, built around real rice heat-stress candidate genes
reported in the literature (e.g. `OsHSP70`, `OsHSFA2d`, `OsHDAC6`, `OsSR45`, `OsTRBF1`,
`OsDREB2A`, `OsC3H60`).

| File | Description |
| --- | --- |
| `sample_metadata.csv` | 16 samples: 2 cultivars (`Tolerant_Cultivar`, `Sensitive_Cultivar`) x 4 conditions (Control 0h; Heat 1h, 3h, 24h) x 2 replicates. |
| `gene_expression.csv` | 12 genes x 16 samples, simulated expression values with heat-response kinetics and a stronger/sustained response in the tolerant cultivar. |
| `splicing_events.csv` | 9 genes with a splicing event type (intron retention, exon skipping, alternative 3'/5' splice site) plus control/heat PSI (Percent Spliced In) and delta PSI. |
| `official_project_candidate_markers.csv` | Curated candidate-gene annotation table (function, validation route, why it matters) used by the Interview & Validation page. |
| `thermotolerance_phenotype_demo.csv` | Demo phenotype scores (survival, chlorophyll, photosynthesis, ROS damage, antioxidant defense, biomass, panicle fertility) by cultivar and condition, used in the Breeding Report. |
| `rice_heat_timecourse_demo.csv`, `alternative_splicing_events_demo.csv`, `synthetic_rice_heat_stress_candidates.csv` | Legacy inputs used only by the standalone CLI script `src/rank_candidates.py`. |

**PSI explained simply:** PSI shows how much a particular splice form is used. If PSI changes
strongly under heat, that gene may be post-transcriptionally regulated during heat stress.

## Methods Workflow

```text
Rice samples -> Heat treatment -> Gene expression matrix -> Differential expression analysis
            -> Alternative-splicing (PSI) analysis -> ML classifier + feature importance
            -> Combined candidate score -> Ranked candidate genes -> Breeding recommendation
```

1. **Differential expression** (`utils/analysis.py`) - compares Control vs Heat samples per gene
   using mean expression, log2 fold change, and a Welch's t-test p-value.
2. **Alternative splicing** (`data/splicing_events.csv`) - control PSI, heat PSI, and delta PSI per
   gene and event type.
3. **Machine learning** (`utils/ml_model.py`) - transposes the gene x sample matrix into a sample x
   gene feature table, then trains a Random Forest classifier (Control vs Heat, or Tolerant vs
   Sensitive) and extracts feature importance, a confusion matrix, and an ROC curve.
4. **Candidate scoring** (`utils/scoring.py`) - combines normalized expression change, p-value
   strength, splicing delta, ML importance, and a known heat/stress function score into one
   candidate score (see formula below).
5. **Breeding interpretation** (`pages/7_Breeding_Report.py`) - maps top candidates to a breeding
   value category and generates a downloadable report.

## Candidate Scoring Formula

Each component is min-max normalized to 0-1 before weighting (weights are adjustable in the
Candidate Ranking page and sum to 1):

| Component | Default weight |
| --- | --- |
| Differential expression strength (\|log2FC\|) | 30% |
| Statistical significance (-log10 p-value) | 20% |
| Alternative splicing change (delta PSI) | 20% |
| ML feature importance | 20% |
| Known heat/stress function | 10% |

```text
candidate_score = 100 x (
    0.30 x expression_norm
  + 0.20 x pvalue_norm
  + 0.20 x splicing_norm
  + 0.20 x ml_importance_norm
  + 0.10 x known_function_score
)
```

Output genes are **prioritized candidates**, not confirmed regulators. They are intended for
follow-up through qRT-PCR, RT-PCR isoform assays, CRISPR-Cas9, overexpression, or breeding-marker
validation.

## Dashboard Pages

| # | Page | What it shows |
| --- | --- | --- |
| 1 | **Project Overview** (`app.py`) | Research problem, core question, hypothesis, pipeline, and how to read the dashboard. |
| 2 | **Dataset Explorer** | Sample/gene/splicing summary counts and filters by cultivar, treatment, and time point. |
| 3 | **Gene Expression** | Top up/down genes, log2 fold change bar charts, a volcano plot, and an expression heatmap. |
| 4 | **Alternative Splicing** | Delta PSI bar chart, control-vs-heat PSI scatter plot, and the full splicing event table. |
| 5 | **Machine Learning** | Random Forest classifier (Control vs Heat, or Tolerant vs Sensitive), accuracy, ROC AUC, confusion matrix, and feature importance. |
| 6 | **Candidate Ranking** | Adjustable scoring weights and the final ranked candidate-gene table and chart. |
| 7 | **Breeding Report** | Breeding-value interpretation per candidate type, phenotype comparison chart, and a downloadable candidate report (TXT + CSV). |
| 8 | **Interview & Validation** | Professor profile, validation-route table, and the interview pitch script. |

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
    interview_script.md           # 45-second pitch, longer explanation, smart questions to ask
    methods_plan.md               # full-scale RNA-seq methods plan for future work
    professor_profile.md          # Prof. Calixto background and official project details
    research_sources.md           # sources used to align this project with the lab
    streamlit_deploy.md           # deployment checklist
```

## Tech Stack

| Part | Tool |
| --- | --- |
| Dashboard | Streamlit (multi-page) |
| Data handling | Pandas, NumPy |
| Graphs | Plotly |
| Machine learning | Scikit-learn (Random Forest, train/test split, ROC/AUC) |
| Statistics | SciPy (Welch's t-test) |
| Deployment | Streamlit Community Cloud |
| Code storage | GitHub |

## Running The Project

### Streamlit dashboard (main demo)

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Legacy CLI ranking script

No external Python packages are required.

```bash
python src/rank_candidates.py --focus balanced
python src/rank_candidates.py --focus splicing
python src/rank_candidates.py --focus memory
python src/rank_candidates.py --focus breeding
```

### Static HTML backup demo

Open `web/index.html` directly in a browser. The Streamlit dashboard is the primary demo; this is
a fallback if Streamlit is unavailable.

## Deployment

See [`docs/streamlit_deploy.md`](docs/streamlit_deploy.md) for the full checklist. Short version:
push this repository to GitHub, connect it on Streamlit Community Cloud, and set the main file path
to `app.py` (pages under `pages/` are auto-discovered).

## Limitations

- All sample, expression, and splicing values are synthetic and generated for demonstration
  purposes; they are not real RNA-seq results.
- The dataset is intentionally small (16 samples, 12 genes), so ML accuracy/AUC figures are
  illustrative of the workflow, not a validated biological finding.
- Candidate scores reflect a transparent, adjustable weighting scheme, not a peer-reviewed
  ranking method.

## Future Work

- Replace synthetic data with public RNA-seq reanalysis (e.g. dataset `SRP190858`, used in
  Prof. Calixto's group's prior heat-stress work) or lab-generated rice heat-stress samples.
- Add a real differential-splicing tool (rMATS, SUPPA2, or MAJIQ) in place of the demo PSI table.
- Extend candidate scoring with co-expression network features (e.g. via WGCNA or NetworkX).
- Connect ranked candidates to an actual validation pipeline: qRT-PCR primers, CRISPR-Cas9 guide
  design, or overexpression vector planning.
