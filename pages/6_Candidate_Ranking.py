from __future__ import annotations

import plotly.express as px
import streamlit as st

from utils.analysis import differential_expression
from utils.data_loader import load_gene_expression, load_sample_metadata, load_splicing_events
from utils.ml_model import build_feature_matrix, train_classifier
from utils.scoring import DEFAULT_WEIGHTS, compute_candidate_scores
from utils.style import inject_css

st.set_page_config(page_title="Candidate Ranking - RiceHeat-AS AI", layout="wide")
inject_css()

st.title("Candidate Gene Ranking")
st.write(
    "This page combines differential expression, alternative splicing, and machine-learning feature "
    "importance into a single candidate score. These genes are **prioritized candidates**, not "
    "confirmed regulators."
)

metadata = load_sample_metadata()
expr = load_gene_expression()
splicing = load_splicing_events()

diff = differential_expression(expr, metadata)
features, _ = build_feature_matrix(expr, metadata)
features = features.reindex(metadata.sample_id)
labels = metadata.set_index("sample_id")["treatment"].reindex(features.index)
ml_result = train_classifier(features, labels)

st.markdown("### Scoring Weights")
w1, w2, w3, w4, w5 = st.columns(5)
with w1:
    w_expr = st.slider("Expression change", 0.0, 0.6, DEFAULT_WEIGHTS["expression"], 0.05)
with w2:
    w_p = st.slider("P-value strength", 0.0, 0.6, DEFAULT_WEIGHTS["pvalue"], 0.05)
with w3:
    w_splice = st.slider("Splicing change", 0.0, 0.6, DEFAULT_WEIGHTS["splicing"], 0.05)
with w4:
    w_ml = st.slider("ML importance", 0.0, 0.6, DEFAULT_WEIGHTS["ml_importance"], 0.05)
with w5:
    w_func = st.slider("Known function", 0.0, 0.6, DEFAULT_WEIGHTS["known_function"], 0.05)

weights = {
    "expression": w_expr,
    "pvalue": w_p,
    "splicing": w_splice,
    "ml_importance": w_ml,
    "known_function": w_func,
}
total_weight = sum(weights.values()) or 1.0
normalized_weights = {k: v / total_weight for k, v in weights.items()}

ranked = compute_candidate_scores(diff, splicing, ml_result.importance, normalized_weights)

top_n = st.slider("Top candidates to display", 4, len(ranked), 8)

st.markdown("### Final Candidate Score Table")
display_cols = [
    "gene_id", "gene_name", "function", "log2fc", "delta_PSI", "ml_importance", "candidate_score",
]
table = ranked[display_cols].head(top_n).copy()
table.insert(0, "rank", range(1, len(table) + 1))
st.dataframe(table, use_container_width=True, hide_index=True)

fig = px.bar(
    ranked.head(top_n).sort_values("candidate_score"),
    x="candidate_score", y="gene_name", orientation="h", color="function",
    title="Top candidate genes by combined score",
)
fig.update_layout(height=460)
st.plotly_chart(fig, use_container_width=True)

st.session_state["ranked_candidates"] = ranked

st.caption(
    "Candidate scores combine expression change, statistical significance, splicing shift, ML "
    "feature importance, and known heat/stress function. These genes are prioritized for future "
    "validation through qRT-PCR, CRISPR, overexpression, or breeding trials."
)
