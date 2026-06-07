
from __future__ import annotations
import pandas as pd

def apply_interventions(
    nodes: pd.DataFrame,
    interventions: pd.DataFrame,
    capacity_boost: float = 0.15,
    inventory_boost: float = 0.20,
    failure_reduction: float = 0.25,
) -> pd.DataFrame:
    out = nodes.copy()
    ids = set(interventions.node_id.tolist()) if interventions is not None and not interventions.empty else set()
    mask = out.node_id.isin(ids)
    out.loc[mask, "capacity"] *= (1.0 + capacity_boost)
    out.loc[mask, "target_stock"] *= (1.0 + inventory_boost)
    out.loc[mask, "initial_inventory"] *= (1.0 + inventory_boost)
    out.loc[mask, "failure_prob"] *= (1.0 - failure_reduction)
    return out
