
from __future__ import annotations
import pandas as pd

def summarize_simulation(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["scenario", "policy"], as_index=False).agg(
        total_cost=("total_cost", "mean"),
        stockouts=("stockouts", "mean"),
        service_level=("service_level", "mean"),
        collapse_events=("collapse_events", "mean"),
        avg_backorders=("avg_backorders", "mean"),
        avg_inventory=("avg_inventory", "mean"),
        time_to_first_collapse=("time_to_first_collapse", "mean"),
    )

def compare_to_traditional(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for scenario, g in summary.groupby("scenario"):
        base = g[g.policy == "traditional"]
        if base.empty:
            continue
        base_cost = float(base.total_cost.iloc[0])
        for _, r in g.iterrows():
            d = r.to_dict()
            d["cost_reduction_vs_traditional"] = (base_cost - r.total_cost) / base_cost if base_cost else 0.0
            rows.append(d)
    return pd.DataFrame(rows)
