
from __future__ import annotations
import pandas as pd

def build_intervention_ranking(nodes: pd.DataFrame) -> pd.DataFrame:
    df = nodes[nodes.node_type != "customer_region"].copy()
    df["resilience_value_score"] = (
        df["fragility"]
        * df["economic_severity"]
        * (1.0 + df["network_criticality"])
    )
    df["resilience_per_dollar"] = df["resilience_value_score"] / df["k_prevent"]
    return df.sort_values("resilience_per_dollar", ascending=False)[[
        "node_id", "node_type", "capacity", "demand_mean", "failure_prob",
        "initial_inventory", "reorder_point", "target_stock",
        "delta", "utilization", "economic_severity", "network_criticality",
        "fragility", "resilience_value_score", "resilience_per_dollar", "regime"
    ]]
