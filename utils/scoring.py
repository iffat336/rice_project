from __future__ import annotations

import pandas as pd

DEFAULT_WEIGHTS = {
    "expression": 0.30,
    "pvalue": 0.20,
    "splicing": 0.20,
    "ml_importance": 0.20,
    "known_function": 0.10,
}

FUNCTION_SCORES = {
    "heat shock protein": 1.0,
    "heat-shock transcription factor": 1.0,
    "heat-responsive regulator": 0.9,
    "stress-responsive transcription factor": 0.85,
    "epigenetic / splicing regulator": 0.8,
    "zinc-finger splicing-related factor": 0.8,
    "rna-recognition motif splicing candidate": 0.75,
    "serine/arginine-rich splicing factor": 0.75,
    "spliceosome-related factor": 0.75,
    "temperature-signaling regulator": 0.7,
    "antioxidant defense enzyme": 0.6,
}


def _minmax(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    if span == 0:
        return series * 0
    return (series - series.min()) / span


def compute_candidate_scores(
    diff_expr: pd.DataFrame,
    splicing: pd.DataFrame,
    ml_importance: pd.Series,
    weights: dict[str, float] | None = None,
) -> pd.DataFrame:
    weights = weights or DEFAULT_WEIGHTS

    splicing_max = splicing.groupby("gene_name", as_index=False)["delta_PSI"].max()
    importance_df = ml_importance.rename("ml_importance").reset_index().rename(columns={"index": "gene_name"})

    scored = diff_expr.merge(splicing_max, on="gene_name", how="left").merge(
        importance_df, on="gene_name", how="left"
    )
    scored["delta_PSI"] = scored["delta_PSI"].fillna(0)
    scored["ml_importance"] = scored["ml_importance"].fillna(0)
    scored["known_function_score"] = (
        scored["function"].str.lower().map(FUNCTION_SCORES).fillna(0.5)
    )

    scored["expression_norm"] = _minmax(scored["log2fc"].abs())
    scored["pvalue_norm"] = _minmax(scored["neg_log10_p"])
    scored["splicing_norm"] = _minmax(scored["delta_PSI"])
    scored["ml_norm"] = _minmax(scored["ml_importance"])

    scored["candidate_score"] = (
        scored["expression_norm"] * weights["expression"]
        + scored["pvalue_norm"] * weights["pvalue"]
        + scored["splicing_norm"] * weights["splicing"]
        + scored["ml_norm"] * weights["ml_importance"]
        + scored["known_function_score"] * weights["known_function"]
    ) * 100

    return scored.sort_values("candidate_score", ascending=False).reset_index(drop=True)
