from __future__ import annotations

import plotly.express as px
import streamlit as st

from utils.analysis import differential_expression, expression_long
from utils.data_loader import load_gene_expression, load_sample_metadata
from utils.style import inject_css

st.set_page_config(page_title="Gene Expression - RiceHeat-AS AI", layout="wide")
inject_css()

st.title("Gene Expression Analysis")
st.write(
    "This section compares Control (28 C) and Heat (45 C) samples to identify genes whose expression "
    "changes strongly under heat stress."
)

metadata = load_sample_metadata()
expr = load_gene_expression()
diff = differential_expression(expr, metadata)

top_n = st.slider("Number of genes to show", min_value=4, max_value=len(diff), value=8)

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### Top Upregulated Genes")
    up = diff.sort_values("log2fc", ascending=False).head(top_n)
    fig = px.bar(
        up, x="log2fc", y="gene_name", orientation="h", color="log2fc",
        color_continuous_scale="Reds", title="Highest log2 fold change under heat",
    )
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown("#### Top Downregulated / Lowest-Change Genes")
    down = diff.sort_values("log2fc", ascending=True).head(top_n)
    fig = px.bar(
        down, x="log2fc", y="gene_name", orientation="h", color="log2fc",
        color_continuous_scale="Blues_r", title="Lowest log2 fold change under heat",
    )
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Volcano Plot")
fig = px.scatter(
    diff, x="log2fc", y="neg_log10_p", text="gene_name", color="function",
    labels={"log2fc": "log2 fold change (Heat vs Control)", "neg_log10_p": "-log10(p-value)"},
    title="Differential expression: log2FC vs significance",
)
fig.update_traces(textposition="top center")
fig.update_layout(height=480)
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Expression Heatmap")
long_expr = expression_long(expr, metadata)
pivot = long_expr.pivot_table(index="gene_name", columns="sample_id", values="expression")
fig = px.imshow(pivot, aspect="auto", color_continuous_scale="Viridis", labels=dict(color="Expression"))
fig.update_layout(height=480)
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Differential Expression Table")
st.dataframe(
    diff[["gene_id", "gene_name", "function", "mean_control", "mean_heat", "log2fc", "pvalue"]],
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "This section identifies genes whose expression changes strongly under heat stress. Expression "
    "alone is not enough, so splicing and machine-learning ranking are added on the following pages."
)
