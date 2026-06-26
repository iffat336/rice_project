from __future__ import annotations

import streamlit as st

from utils.style import inject_css, metric_card

st.set_page_config(page_title="RiceHeat-AS AI Dashboard", layout="wide")
inject_css()

st.markdown(
    """
    <div class="hero">
      <h1>RiceHeat-AS AI Dashboard</h1>
      <p>
        AI-Assisted Gene and Splicing Marker Discovery for Heat-Tolerant Rice. A computational
        prototype inspired by Prof. Dr. Cristiane Paula Gomes Calixto's FAPESP project,
        "Transcriptome-wide analysis of rice temperature memory and heat responses," at the
        Institute of Biosciences, University of Sao Paulo.
      </p>
      <div class="tag-row">
        <span>Oryza sativa</span>
        <span>Gene expression</span>
        <span>Alternative splicing</span>
        <span>Machine learning</span>
        <span>Candidate ranking</span>
        <span>Breeding translation</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Research Problem")
st.write(
    "Heat stress reduces rice yield and grain quality. This project uses transcriptomic and "
    "alternative-splicing data to identify candidate genes involved in heat-stress tolerance and "
    "temperature-memory responses, then prioritizes them for future breeding or functional validation."
)

st.markdown("### Core Question")
st.info(
    "Can we use transcriptomic and alternative-splicing data to identify candidate genes associated "
    "with rice heat-stress tolerance and prioritize them for future breeding or functional validation?"
)

st.markdown("### Pipeline")
st.markdown(
    """
    Rice samples &rarr; Heat treatment &rarr; RNA-seq data &rarr; Gene expression analysis &rarr;
    Splicing analysis &rarr; ML model &rarr; Candidate genes &rarr; Breeding recommendation
    """
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Project type", "Prototype", "Computational demo, not a wet-lab project.")
with c2:
    metric_card("Crop", "Rice", "Oryza sativa under high-temperature stress.")
with c3:
    metric_card("Lab fit", "FAPESP 2021-2027", "Prof. Calixto's rice temperature-memory project.")
with c4:
    metric_card("Output", "Candidate genes", "Ranked for breeding and validation follow-up.")

st.markdown("### Main Hypothesis")
st.write(
    "Rice heat-stress tolerance is controlled not only by changes in gene-expression levels but also "
    "by post-transcriptional regulation such as alternative splicing. Integrating differential "
    "expression, alternative-splicing indicators, and machine-learning feature ranking can help "
    "prioritize candidate genes for future validation and climate-resilient rice breeding."
)

st.markdown("### How To Read This Dashboard")
st.markdown(
    """
    - **Dataset Explorer** &mdash; browse the demonstration samples, genes, and filters.
    - **Gene Expression** &mdash; top heat-responsive genes, fold change, and volcano plot.
    - **Alternative Splicing** &mdash; PSI shifts between control and heat conditions.
    - **Machine Learning** &mdash; a Random Forest classifier and feature importance ranking.
    - **Candidate Ranking** &mdash; the combined scoring table and final gene priority list.
    - **Breeding Report** &mdash; breeding interpretation and a downloadable candidate report.
    - **Interview & Validation** &mdash; lab background, validation routes, and the interview pitch.
    """
)

st.caption(
    "Important: the data in this prototype is synthetic demonstration data designed to explain the "
    "workflow. It is not a wet-lab result. Real research would require RNA-seq reanalysis, "
    "lab-generated rice stress samples, or both."
)
