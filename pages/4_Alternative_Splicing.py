from __future__ import annotations

import plotly.express as px
import streamlit as st

from utils.data_loader import load_splicing_events
from utils.style import inject_css

st.set_page_config(page_title="Alternative Splicing - RiceHeat-AS AI", layout="wide")
inject_css()

st.title("Alternative Splicing Analysis")
st.write(
    "Prof. Calixto's research emphasizes that heat stress affects not only gene expression but also "
    "transcript isoform usage through alternative splicing. PSI (Percent Spliced In) shows how much a "
    "particular splice form is used. A large shift in PSI under heat suggests the gene is "
    "post-transcriptionally regulated during heat stress."
)

splicing = load_splicing_events()

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### Delta PSI by Gene")
    fig = px.bar(
        splicing.sort_values("delta_PSI", ascending=False),
        x="delta_PSI", y="gene_name", orientation="h", color="splicing_event",
        title="Splicing change magnitude (Heat vs Control)",
        labels={"delta_PSI": "Delta PSI", "gene_name": "Gene"},
    )
    fig.update_layout(height=440)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown("#### Control vs Heat PSI")
    fig = px.scatter(
        splicing, x="control_PSI", y="heat_PSI", color="splicing_event", size="delta_PSI",
        hover_name="gene_name", title="Heat PSI vs control PSI",
        labels={"control_PSI": "Control PSI", "heat_PSI": "Heat PSI"},
    )
    fig.add_shape(type="line", x0=0, y0=0, x1=1, y1=1, line=dict(dash="dot", color="gray"))
    fig.update_layout(height=440)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Gene-Wise Splicing Event Table")
st.dataframe(
    splicing.sort_values("delta_PSI", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Her 2021 rice paper found 17,143 heat-response genes and 2,162 differentially alternatively "
    "spliced genes, showing that alternative splicing is a major component of rice heat-stress response."
)
