
from __future__ import annotations
import numpy as np
import pandas as pd

def add_near_critical_metrics(nodes: pd.DataFrame) -> pd.DataFrame:
    df = nodes.copy()
    df["effective_capacity"] = (1.0 - df["failure_prob"]) * df["capacity"]
    df["delta"] = df["effective_capacity"] - df["demand_mean"]
    df["utilization"] = df["demand_mean"] / df["capacity"]
    df["economic_severity"] = df["k_fail"] / df["k_prevent"]
    df["fragility"] = 1.0 / (1.0 + np.maximum(df["delta"], 0.0))
    df["regime"] = pd.cut(
        df["delta"],
        bins=[-1e12, 0, 5, 20, 1e12],
        labels=["overloaded", "critical", "near_critical", "safe"],
    )
    return df
