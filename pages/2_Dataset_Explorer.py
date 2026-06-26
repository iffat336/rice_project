from __future__ import annotations

import streamlit as st

from utils.data_loader import load_gene_expression, load_sample_metadata, load_splicing_events
from utils.style import inject_css, metric_card

st.set_page_config(page_title="Dataset Explorer - RiceHeat-AS AI", layout="wide")
inject_css()

st.title("Dataset Explorer")
st.write(
    "This prototype dataset is a small demonstration RNA-seq table built around real heat-stress "
    "candidate genes reported in rice transcriptome studies. It is not a full experiment; it is "
    "sized to explain the analysis workflow."
)

metadata = load_sample_metadata()
expr = load_gene_expression()
splicing = load_splicing_events()

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Total samples", str(len(metadata)), "Across cultivars, treatments, and time points.")
with c2:
    metric_card("Genes profiled", str(len(expr)), "Heat-response and splicing-related candidates.")
with c3:
    metric_card("Heat samples", str((metadata.treatment == "Heat").sum()), "Samples exposed to 45 C.")
with c4:
    metric_card("Control samples", str((metadata.treatment == "Control").sum()), "Samples kept at 28 C.")

st.markdown("### Filters")
f1, f2, f3 = st.columns(3)
with f1:
    cultivar_filter = st.multiselect("Cultivar", sorted(metadata.cultivar.unique()), default=list(metadata.cultivar.unique()))
with f2:
    treatment_filter = st.multiselect("Treatment", sorted(metadata.treatment.unique()), default=list(metadata.treatment.unique()))
with f3:
    time_filter = st.multiselect("Time point", sorted(metadata.time_point.unique(), key=lambda t: int(t.rstrip("h"))), default=list(metadata.time_point.unique()))

filtered = metadata[
    metadata.cultivar.isin(cultivar_filter)
    & metadata.treatment.isin(treatment_filter)
    & metadata.time_point.isin(time_filter)
]

st.markdown(f"### Sample Metadata ({len(filtered)} of {len(metadata)} samples)")
st.dataframe(filtered, use_container_width=True, hide_index=True)

st.markdown("### Gene Panel")
st.dataframe(expr[["gene_id", "gene_name", "function"]], use_container_width=True, hide_index=True)

st.markdown("### Splicing Event Panel")
st.dataframe(splicing, use_container_width=True, hide_index=True)

st.caption("Cultivar and tolerance labels are simulated for this prototype and clearly marked as demonstration data.")
