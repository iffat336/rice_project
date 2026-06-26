from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.analysis import differential_expression
from utils.data_loader import load_gene_expression, load_phenotypes, load_sample_metadata, load_splicing_events
from utils.ml_model import build_feature_matrix, train_classifier
from utils.scoring import DEFAULT_WEIGHTS, compute_candidate_scores
from utils.style import inject_css

st.set_page_config(page_title="Breeding Report - RiceHeat-AS AI", layout="wide")
inject_css()

st.title("Breeding Interpretation & Report")
st.write(
    "My background in Plant Breeding and Genetics helps me interpret these molecular results in the "
    "context of cultivar improvement. The dashboard does not replace field trials; it helps "
    "prioritize genes and traits for future validation."
)

metadata = load_sample_metadata()
expr = load_gene_expression()
splicing = load_splicing_events()
phenotypes = load_phenotypes()

if "ranked_candidates" in st.session_state:
    ranked = st.session_state["ranked_candidates"]
else:
    diff = differential_expression(expr, metadata)
    features, _ = build_feature_matrix(expr, metadata)
    features = features.reindex(metadata.sample_id)
    labels = metadata.set_index("sample_id")["treatment"].reindex(features.index)
    ml_result = train_classifier(features, labels)
    ranked = compute_candidate_scores(diff, splicing, ml_result.importance, DEFAULT_WEIGHTS)

st.markdown("### Breeding Value By Candidate Type")
breeding_value = {
    "heat shock protein": "Direct stress protection",
    "heat-shock transcription factor": "Control of downstream stress genes",
    "stress-responsive transcription factor": "Control of downstream stress genes",
    "epigenetic / splicing regulator": "Possible heat-stress memory control",
    "zinc-finger splicing-related factor": "Regulation of stress transcript isoforms",
    "rna-recognition motif splicing candidate": "Regulation of stress transcript isoforms",
    "serine/arginine-rich splicing factor": "Regulation of stress transcript isoforms",
    "spliceosome-related factor": "Regulation of stress transcript isoforms",
    "temperature-signaling regulator": "Marker for temperature-memory breeding",
    "antioxidant defense enzyme": "Direct stress protection",
    "heat-responsive regulator": "Possible heat-stress memory control",
}
breeding_table = ranked[["gene_name", "function"]].head(10).copy()
breeding_table["breeding_value"] = breeding_table["function"].str.lower().map(breeding_value).fillna(
    "Candidate for further annotation"
)
st.dataframe(breeding_table, use_container_width=True, hide_index=True)

st.markdown("### Phenotype Comparison (Tolerant vs Sensitive)")
fig = px.bar(
    phenotypes, x="trait", y="value", color="cultivar_type", barmode="group", facet_col="condition",
    labels={"value": "Relative score", "trait": "Trait", "cultivar_type": "Cultivar"},
    title="Demo phenotype comparison across heat-stress conditions",
)
fig.update_layout(height=430, legend_orientation="h")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Suggested Validation Methods")
st.markdown(
    """
    - **qRT-PCR** to confirm expression changes between tolerant and sensitive cultivars.
    - **RT-PCR / isoform assays** to validate heat-responsive alternative-splicing events.
    - **CRISPR-Cas9 or overexpression lines** to test candidate regulators directly.
    - **Field heat-stress phenotyping** to connect candidates with survival, photosynthesis, and grain traits.
    """
)

st.markdown("### Download Candidate Gene Report")
top10 = ranked.head(10)
report_lines = [
    "RiceHeat-AS AI - Candidate Gene Report",
    f"Generated: {date.today().isoformat()}",
    "",
    "Project: AI-Assisted Gene and Splicing Marker Discovery for Heat-Tolerant Rice",
    "Dataset: synthetic prototype, 16 samples, 12 genes, 9 splicing events",
    "",
    "Top 10 Candidate Genes:",
]
for rank, row in enumerate(top10.itertuples(), start=1):
    report_lines.append(
        f"{rank}. {row.gene_name} ({row.gene_id}) - {row.function} - score {row.candidate_score:.1f}"
    )
report_lines += [
    "",
    "Top Splicing Events:",
]
for row in splicing.sort_values("delta_PSI", ascending=False).head(5).itertuples():
    report_lines.append(f"- {row.gene_name}: {row.splicing_event}, delta PSI {row.delta_PSI:.2f}")
report_lines += [
    "",
    "Breeding Recommendation:",
    "Prioritize heat-shock and splicing-factor candidates for qRT-PCR validation, then move top",
    "candidates to CRISPR-Cas9 or overexpression testing before field heat-stress phenotyping.",
    "",
    "Limitations:",
    "This is a synthetic prototype dataset built to demonstrate the analysis workflow. It does not",
    "represent confirmed biological results. Real validation requires RNA-seq reanalysis and",
    "lab-generated rice heat-stress samples.",
    "",
    "Future Work:",
    "Replace synthetic data with public RNA-seq reanalysis (e.g. SRP190858) or lab-generated samples,",
    "and extend the candidate score with co-expression network features.",
]
report_text = "\n".join(report_lines)

st.download_button(
    "Download Candidate Gene Report (TXT)",
    data=report_text.encode("utf-8"),
    file_name="riceheat_as_ai_candidate_report.txt",
    mime="text/plain",
)
st.download_button(
    "Download Ranked Candidate Table (CSV)",
    data=ranked.to_csv(index=False).encode("utf-8"),
    file_name="riceheat_as_ai_candidate_ranking.csv",
    mime="text/csv",
)
