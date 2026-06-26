from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


def differential_expression(expr: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    """Compare Control vs Heat samples for every gene and return fold-change stats."""
    control_samples = metadata.loc[metadata.treatment == "Control", "sample_id"].tolist()
    heat_samples = metadata.loc[metadata.treatment == "Heat", "sample_id"].tolist()

    records = []
    for _, row in expr.iterrows():
        control_vals = row[control_samples].astype(float).to_numpy()
        heat_vals = row[heat_samples].astype(float).to_numpy()
        mean_control = control_vals.mean()
        mean_heat = heat_vals.mean()
        log2fc = np.log2((mean_heat + 1) / (mean_control + 1))
        _, pvalue = ttest_ind(heat_vals, control_vals, equal_var=False)
        records.append(
            {
                "gene_id": row.gene_id,
                "gene_name": row.gene_name,
                "function": row.function,
                "mean_control": round(mean_control, 1),
                "mean_heat": round(mean_heat, 1),
                "log2fc": round(log2fc, 2),
                "pvalue": round(pvalue, 4),
                "neg_log10_p": round(-np.log10(max(pvalue, 1e-6)), 2),
            }
        )
    return pd.DataFrame(records).sort_values("log2fc", ascending=False)


def expression_long(expr: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    """Reshape the wide gene x sample matrix into a long table joined with sample metadata."""
    sample_cols = metadata["sample_id"].tolist()
    long_df = expr.melt(
        id_vars=["gene_id", "gene_name", "function"],
        value_vars=sample_cols,
        var_name="sample_id",
        value_name="expression",
    )
    return long_df.merge(metadata, on="sample_id")
