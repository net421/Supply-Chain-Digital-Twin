
from __future__ import annotations
import pandas as pd

def select_traditional_interventions(nodes: pd.DataFrame, budget: float) -> pd.DataFrame:
    df = nodes[nodes.node_type != "customer_region"].copy()
    df["traditional_score"] = (
        0.45 * df["utilization"].rank(pct=True)
        + 0.25 * df["failure_prob"].rank(pct=True)
        + 0.20 * (df["demand_mean"] / (df["initial_inventory"] + 1)).rank(pct=True)
        + 0.10 * df["k_fail"].rank(pct=True)
    )
    df = df.sort_values("traditional_score", ascending=False)
    selected = []
    spent = 0.0
    for _, r in df.iterrows():
        cost = float(r.k_prevent)
        if spent + cost <= budget:
            selected.append(r)
            spent += cost
    return pd.DataFrame(selected)
