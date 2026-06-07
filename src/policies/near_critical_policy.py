
from __future__ import annotations
import pandas as pd

def select_near_critical_interventions(nodes: pd.DataFrame, budget: float) -> pd.DataFrame:
    df = nodes[nodes.node_type != "customer_region"].copy()
    df["near_critical_score"] = (
        df["fragility"]
        * df["economic_severity"].rank(pct=True)
        * (1.0 + df["network_criticality"])
    )
    df = df.sort_values("near_critical_score", ascending=False)
    selected = []
    spent = 0.0
    for _, r in df.iterrows():
        cost = float(r.k_prevent)
        if spent + cost <= budget:
            selected.append(r)
            spent += cost
    return pd.DataFrame(selected)
