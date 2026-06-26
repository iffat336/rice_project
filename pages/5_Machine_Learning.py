from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import load_gene_expression, load_sample_metadata
from utils.ml_model import build_feature_matrix, train_classifier
from utils.style import inject_css

st.set_page_config(page_title="Machine Learning - RiceHeat-AS AI", layout="wide")
inject_css()

st.title("Machine Learning Classifier")
st.write(
    "I used machine learning not as final biological proof, but as a prioritization tool to identify "
    "genes and transcript features that best separate heat-stress response classes."
)

metadata = load_sample_metadata()
expr = load_gene_expression()
features, gene_names = build_feature_matrix(expr, metadata)
features = features.reindex(metadata.sample_id)

target = st.selectbox(
    "Prediction target",
    ["Control vs Heat (treatment)", "Tolerant vs Sensitive (tolerance_group)"],
)
label_col = "treatment" if target.startswith("Control") else "tolerance_group"
labels = metadata.set_index("sample_id")[label_col].reindex(features.index)

result = train_classifier(features, labels)

m1, m2, m3 = st.columns(3)
m1.metric("Model", "Random Forest")
m2.metric("Test accuracy", f"{result.accuracy * 100:.1f}%")
m3.metric("ROC AUC", f"{result.roc_auc:.2f}")

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### Feature Importance")
    imp = result.importance.head(10).reset_index()
    imp.columns = ["gene", "importance"]
    fig = px.bar(imp, x="importance", y="gene", orientation="h", title="Top genes driving the classifier")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown("#### Confusion Matrix")
    fig = go.Figure(
        data=go.Heatmap(
            z=result.confusion,
            x=[f"Predicted {c}" for c in result.classes],
            y=[f"Actual {c}" for c in result.classes],
            colorscale="Greens",
            showscale=False,
            text=result.confusion,
            texttemplate="%{text}",
        )
    )
    fig.update_layout(height=400, title="Test-set confusion matrix")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("#### ROC Curve")
roc_fig = go.Figure()
roc_fig.add_trace(go.Scatter(x=result.fpr, y=result.tpr, mode="lines", name=f"ROC (AUC = {result.roc_auc:.2f})"))
roc_fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(dash="dot"), name="Random baseline"))
roc_fig.update_layout(height=420, xaxis_title="False positive rate", yaxis_title="True positive rate")
st.plotly_chart(roc_fig, use_container_width=True)

st.caption(
    "Sample size in this prototype is small, so accuracy and AUC are illustrative of the workflow "
    "rather than a validated biological result."
)
