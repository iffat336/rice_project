from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


@st.cache_data
def load_sample_metadata() -> pd.DataFrame:
    return pd.read_csv(DATA / "sample_metadata.csv")


@st.cache_data
def load_gene_expression() -> pd.DataFrame:
    return pd.read_csv(DATA / "gene_expression.csv")


@st.cache_data
def load_splicing_events() -> pd.DataFrame:
    return pd.read_csv(DATA / "splicing_events.csv")


@st.cache_data
def load_candidate_markers() -> pd.DataFrame:
    return pd.read_csv(DATA / "official_project_candidate_markers.csv")


@st.cache_data
def load_phenotypes() -> pd.DataFrame:
    return pd.read_csv(DATA / "thermotolerance_phenotype_demo.csv")


def sample_columns(metadata: pd.DataFrame) -> list[str]:
    return metadata["sample_id"].tolist()
