from __future__ import annotations

import streamlit as st

from utils.data_loader import load_candidate_markers
from utils.style import inject_css, metric_card

st.set_page_config(page_title="Interview & Validation - RiceHeat-AS AI", layout="wide")
inject_css()

st.title("Interview & Validation Notes")

profile, validation, pitch = st.tabs(["Professor Profile", "Validation Plan", "Interview Pitch"])

with profile:
    st.subheader("Prof. Dr. Cristiane Paula Gomes Calixto")
    st.write(
        "Official IB-USP pages list Prof. Cristiane Calixto in the Department of Botany at the "
        "Institute of Biosciences, University of Sao Paulo. The postgraduate Botany faculty page "
        "describes her group as studying the complexity of plant gene-expression regulation in "
        "response to abiotic stresses, integrating post-transcriptional and epigenetic mechanisms."
    )

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        metric_card("Institution", "IB-USP", "Institute of Biosciences, University of Sao Paulo.")
    with p2:
        metric_card("Department", "Botany", "Department of Botany, University of Sao Paulo.")
    with p3:
        metric_card("Research group", "Abiotic stress", "Gene-expression regulation under plant stress.")
    with p4:
        metric_card("Grant period", "2021-2027", "FAPESP Young Investigator Grant 19/13158-8.")

    st.markdown("### Academic Background")
    st.markdown(
        """
        - B.Sc. in Biological Sciences, University of Sao Paulo, 2004.
        - M.Sc. in Genetics, University of Sao Paulo, 2008.
        - PhD in Plant Sciences, University of Dundee, UK, 2014.
        - Postdoctoral Research Assistant, University of Dundee, UK, 2014-2017.
        """
    )

    st.markdown("### Research Expertise")
    st.markdown(
        """
        - Plant molecular biology and regulation of gene expression.
        - Transcriptome analysis and next-generation sequencing.
        - Alternative splicing and post-transcriptional regulation.
        - Non-coding RNAs, RNAi, phylogenetic analysis, and circadian clock genes.
        - Temperature stress, rice heat response, and temperature memory.
        - Candidate validation through CRISPR-Cas9 and overexpression strategies.
        """
    )

    st.markdown("### Official Links")
    st.markdown(
        """
        - [IB-USP faculty page](https://www.ib.usp.br/botanica/info/corpo-docente/624-cristiane-calixto.html)
        - [IB-USP Postgraduate Botany faculty page](https://posbotanica.ib.usp.br/pt/institucional/docentes.html)
        - [FAPESP researcher profile](https://bv.fapesp.br/pt/pesquisador/179334/cristiane-paula-gomes-calixto/)
        - [IB-USP growth chamber page](https://www.ib.usp.br/botanica/30-depto-de-botanica/3292-camara-growth-house-de-crescimento-de-plantas.html)
        """
    )

with validation:
    st.subheader("Candidate Validation Plan")
    st.write("The strongest interview point is that AI only prioritizes. Functional validation remains biological.")

    markers = load_candidate_markers()
    validation_cols = ["gene", "candidate_area", "why_it_matters", "validation_route", "interview_note"]
    st.dataframe(markers[validation_cols], use_container_width=True, hide_index=True)

    st.markdown("### Validation Routes")
    st.markdown(
        """
        - **qRT-PCR:** Confirm expression changes in tolerant and sensitive cultivars.
        - **RT-PCR / isoform assays:** Validate heat-responsive alternative-splicing events.
        - **Co-expression modules:** Identify splicing factors, epigenetic regulators, and target modules.
        - **CRISPR-Cas9:** Test loss-of-function candidates such as OsTRBF1, LOC_Os02g40900, or LOC_Os05g30140.
        - **Overexpression:** Compare OsHDAC6 alternative isoforms or other strong transcript candidates.
        - **Breeding translation:** Connect markers with survival, photosynthesis, antioxidant defense, panicle fertility, and grain traits.
        """
    )

with pitch:
    st.subheader("Monday Interview Pitch")
    st.markdown(
        """
        <div class="script-box">
        I developed a prototype called RiceHeat-AS AI, inspired by Prof. Calixto's ongoing project on
        rice temperature memory and heat responses. The goal is to integrate gene-expression,
        alternative-splicing, and machine-learning analysis to prioritize candidate genes for
        heat-stress tolerance in rice. The app allows users to compare control and heat-stress
        conditions, visualize gene-expression changes, examine splicing shifts, run a classifier,
        and generate a ranked list of candidate genes for future validation and breeding.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### How I Would Explain The Demo")
    st.markdown(
        """
        This Streamlit demo is a prototype of my research thinking. It shows how I would organize the
        project: first compare tolerant and sensitive rice cultivars, then analyze gene expression and
        alternative-splicing data, and finally use machine-learning scoring to prioritize candidate
        genes for validation.

        I understand that the AI model does not prove gene function. It helps narrow complex
        transcriptome data into testable biological hypotheses for qPCR, isoform validation, CRISPR,
        overexpression, and breeding use.
        """
    )

    st.markdown("### Smart Questions To Ask Her")
    st.markdown(
        """
        1. Would your lab prefer this sub-project to start with public RNA-seq reanalysis (e.g. SRP190858) or with lab-generated samples?
        2. Which layer is currently most important in your project: gene expression, alternative splicing, or temperature memory?
        3. Are OsTRBF1, LOC_Os02g40900, LOC_Os05g30140, or OsHDAC6 still active candidate directions in the lab?
        4. Which computational tools should I strengthen first for your group: R/Bioconductor, RNA-seq pipelines, differential splicing, or co-expression networks?
        5. Could ML-based prioritization be useful before selecting candidates for CRISPR or overexpression?
        """
    )

st.caption("Note: this demo uses synthetic values to communicate a research workflow. It is not claiming original biological results.")
