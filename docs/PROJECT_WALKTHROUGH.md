# RiceHeat-AS AI: Full Step-by-Step Walkthrough

This file explains, in plain language, every step that went into building and deploying this
project — from the original idea to the live link you can show in your interview. Read it top to
bottom once and you should be able to explain any part of the project confidently.

---

## Step 1: The Idea

You wanted a project that connects directly to Prof. Calixto's FAPESP research, *"Transcriptome-wide
analysis of rice temperature memory and heat responses."* Since you can't run a real wet-lab
experiment before the interview, the plan was to build a **computational prototype**: a small,
honest, synthetic dataset plus a dashboard that demonstrates how you would *think* about the
biological problem and *organize* an analysis pipeline.

The agreed scope: gene expression + alternative splicing + machine learning + candidate-gene
ranking + breeding interpretation, wrapped in a Streamlit app.

## Step 2: Designing The Demo Dataset

Real RNA-seq data takes weeks to generate. Instead, three CSV files were created with a Python
script (`gen_data.py`, run once and discarded — the *output* is what matters, not the generator):

1. **`sample_metadata.csv`** — describes 16 fake rice samples: two cultivars
   (`Tolerant_Cultivar`, `Sensitive_Cultivar`), under Control (28°C) or Heat (45°C) at different
   time points (0h, 1h, 3h, 24h), with 2 replicates each.
2. **`gene_expression.csv`** — 12 genes × those 16 samples. The numbers aren't random: genes known
   from real rice heat-stress literature (`OsHSP70`, `OsHSFA2d`, `OsHDAC6`, `OsSR45`, `OsTRBF1`,
   `OsDREB2A`, `OsC3H60`, etc.) were given a simulated expression curve that rises with heat
   exposure time and rises *more* in the tolerant cultivar — mimicking what a real heat-response
   gene would look like.
3. **`splicing_events.csv`** — for 9 of those genes, a splicing event type (intron retention, exon
   skipping, alternative splice site) plus a **PSI** value before and after heat. PSI = "Percent
   Spliced In," i.e. how often a particular version of the gene's transcript is used. A big jump in
   PSI under heat means the gene's RNA processing changed, not just its expression level.

Why this matters for the interview: it shows you understand that heat tolerance isn't only about
"gene expression goes up or down" — it's also about *which version* of the transcript gets made,
which is exactly what Prof. Calixto's lab studies.

## Step 3: Building the Analysis Logic (`utils/`)

Four small Python modules do the actual science, separated from the page-display code so the logic
is reusable and testable:

- **`data_loader.py`** — just reads the CSV files (with Streamlit's caching so the app doesn't
  re-read files on every click).
- **`analysis.py`** — compares Control vs. Heat samples for every gene: computes the average
  expression in each group, the **log2 fold change** (how many "doublings" the expression went up
  or down), and a **p-value** (a statistics test — Welch's t-test — that tells you how likely this
  difference is *not* due to random noise).
- **`ml_model.py`** — turns the gene × sample table sideways (samples become rows, genes become
  columns) so it can be fed into a classifier. Trains a **Random Forest** (a machine-learning model
  that builds many decision trees and votes) to predict either "Control vs Heat" or "Tolerant vs
  Sensitive" from the gene expression values, then reports accuracy, a confusion matrix, an ROC
  curve, and which genes were most useful for the prediction (**feature importance**).
- **`scoring.py`** — combines everything (expression change, p-value, splicing change, ML
  importance, and known stress-related function) into one final **candidate score per gene**,
  using a transparent weighted formula (see the README for the exact percentages).

## Step 4: Building The Dashboard (8 Pages)

Streamlit automatically turns every file inside a `pages/` folder into a page in the sidebar. Each
page is a thin layer that calls the `utils/` functions and draws charts with Plotly:

| Page | What you'd say it does in the interview |
| --- | --- |
| **1. Project Overview** (`app.py`) | "This is the landing page — it states the research question and the analysis pipeline." |
| **2. Dataset Explorer** | "Here I show what the demo dataset looks like, with filters by cultivar, treatment, and time point." |
| **3. Gene Expression** | "This compares Control vs Heat for every gene — fold change, a volcano plot, and a heatmap." |
| **4. Alternative Splicing** | "This shows PSI shifts — which genes change their spliced transcript form under heat." |
| **5. Machine Learning** | "A Random Forest classifier — not to prove biology, but to rank which genes carry the most predictive signal." |
| **6. Candidate Ranking** | "All the previous signals combined into one adjustable score, so you can see how the ranking changes if you weight splicing more or expression more." |
| **7. Breeding Report** | "Translates the top candidates into breeding-relevant categories and lets you download a report." |
| **8. Interview & Validation** | "Background on Prof. Calixto's lab, validation routes (qPCR, CRISPR, etc.), and my actual interview pitch script." |

## Step 5: Putting It Under Version Control (Git)

The project folder lived inside a much bigger, unrelated git repository (your whole `C:\Users\HP`
folder, which was already tracking a completely different project on GitHub). Pushing from there
directly would have risked sending unrelated personal files to the wrong repository, so instead:

1. `git init` was run **inside** `rice-heat-stress-ai/` only, creating a brand-new, isolated git
   repository scoped to just this project.
2. A `.gitignore` was added so Python's `__pycache__` cache folders never get committed.
3. `git add -A` staged every project file (app, pages, utils, data, docs).
4. `git commit` saved that as the first commit, with a clear message describing what the project
   does.

## Step 6: Pushing To GitHub

1. You created an empty repository on GitHub: `https://github.com/iffat336/rice_project`.
2. `git remote add origin <that URL>` linked the local repo to it.
3. `git branch -M main` made sure the branch was named `main` (GitHub's default).
4. `git push -u origin main` uploaded all 35 files in one go.

Later, the README was rewritten to be a full project summary (objectives, dataset description,
scoring formula, page-by-page guide, tech stack, limitations, future work), committed again, and
pushed the same way — `git add`, `git commit`, `git push`.

You can always see the exact history with:

```bash
git log --oneline
```

## Step 7: Deploying To Streamlit Community Cloud

This part had to happen in your browser since it requires logging into your GitHub account through
Streamlit's website (no command-line tool can do this on your behalf):

1. You went to **share.streamlit.io**, signed in with GitHub.
2. Clicked "Create app," chose the repo `iffat336/rice_project`, branch `main`, and main file
   `app.py` (the file at the repo root — Streamlit auto-detects everything inside `pages/` on its
   own, no need to select those individually).
3. Streamlit Cloud read `requirements.txt`, installed `streamlit`, `pandas`, `numpy`, `plotly`,
   `scikit-learn`, and `scipy`, and started the app.
4. The result: a live URL —
   `https://riceproject-uhenhtxlxaqdcrfmwapizi.streamlit.app/`

## Step 8: Making The App Public

By default a newly deployed app can be restricted to specific viewers. Since you want anyone
(e.g. the interviewer) to open the link without logging in:

1. Open the app, click **"Share"** in the top toolbar.
2. In the dialog, the toggle **"Make this app public"** needs to be switched on (blue).
3. Confirmed working: visiting the link returns a normal `HTTP 200` page, not a login redirect.

(The one confusing moment here: even a fully public Streamlit app shows a brief `303` redirect to
`share.streamlit.io/-/auth/app` on the very first request — that's just Streamlit's session-cookie
handshake, not a real login wall. Following that redirect returns the actual app with status 200.)

## Step 9: How To Run It Yourself, Locally

If you ever want to demo it without internet, or tweak something before the interview:

```bash
cd rice-heat-stress-ai
pip install -r requirements.txt
streamlit run app.py
```

This opens the same 8-page dashboard at `http://localhost:8501` in your default browser.

## Step 10: What To Actually Say In The Interview

Don't lead with the engineering. Lead with the biology, then mention the tool:

> "I built a small computational prototype called RiceHeat-AS AI to demonstrate how I'd approach
> your rice temperature-memory project. It takes simulated gene-expression and alternative-splicing
> data, ranks candidate genes using a transparent scoring system, and connects the output to
> breeding-relevant interpretation. It's not a wet-lab result — it's a demonstration of how I
> structure this kind of problem and where I'd plug in real RNA-seq data."

Then walk them through the dashboard live: Dataset Explorer → Gene Expression → Alternative
Splicing → Machine Learning → Candidate Ranking → Breeding Report. Finish by saying you understand
the AI layer only *prioritizes* candidates; real validation still requires qPCR, CRISPR, or
overexpression work — exactly what's written on the Interview & Validation page.

The full pitch script, longer explanation, and smart questions to ask her are in
[`interview_script.md`](interview_script.md).
