#!/usr/bin/env python3
"""Rank synthetic rice heat-stress candidates for the interview demo."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_rice_heat_stress_candidates.csv"

WEIGHTS = {
    "balanced": {
        "heat_log2fc": 0.32,
        "splicing_delta": 0.26,
        "memory_index": 0.22,
        "breeding_relevance": 0.20,
    },
    "splicing": {
        "heat_log2fc": 0.18,
        "splicing_delta": 0.52,
        "memory_index": 0.18,
        "breeding_relevance": 0.12,
    },
    "memory": {
        "heat_log2fc": 0.22,
        "splicing_delta": 0.20,
        "memory_index": 0.46,
        "breeding_relevance": 0.12,
    },
    "breeding": {
        "heat_log2fc": 0.26,
        "splicing_delta": 0.14,
        "memory_index": 0.18,
        "breeding_relevance": 0.42,
    },
}


def normalize_heat(value: float) -> float:
    """Scale log2 fold change to roughly 0-1 for this small demo dataset."""
    return min(value / 5.0, 1.0)


def score(row: dict[str, str], focus: str) -> float:
    weights = WEIGHTS[focus]
    heat = normalize_heat(float(row["heat_log2fc"]))
    splicing = float(row["splicing_delta"])
    memory = float(row["memory_index"])
    breeding = float(row["breeding_relevance"])

    return (
        heat * weights["heat_log2fc"]
        + splicing * weights["splicing_delta"]
        + memory * weights["memory_index"]
        + breeding * weights["breeding_relevance"]
    ) * 100


def load_candidates() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank rice heat-stress candidate genes.")
    parser.add_argument(
        "--focus",
        choices=sorted(WEIGHTS),
        default="balanced",
        help="Ranking emphasis for the interview explanation.",
    )
    parser.add_argument("--top", type=int, default=6, help="Number of candidates to show.")
    args = parser.parse_args()

    ranked = sorted(
        (
            {
                **candidate,
                "score": round(score(candidate, args.focus), 1),
            }
            for candidate in load_candidates()
        ),
        key=lambda item: item["score"],
        reverse=True,
    )

    print(f"# Rice Temperature Memory AI - {args.focus.title()} Ranking")
    print()
    print("| Rank | Gene | Category | Score | Why it matters |")
    print("| --- | --- | --- | ---: | --- |")
    for rank, candidate in enumerate(ranked[: args.top], start=1):
        print(
            "| {rank} | {gene} | {category} | {score} | {rationale} |".format(
                rank=rank,
                gene=candidate["gene"],
                category=candidate["category"],
                score=candidate["score"],
                rationale=candidate["rationale"],
            )
        )


if __name__ == "__main__":
    main()
