
from __future__ import annotations
import time
import numpy as np
import pandas as pd

from .digital_twin import apply_interventions
from .numba_core import simulate_inventory_v3_numba, warmup_numba
from src.policies.traditional_policy import select_traditional_interventions
from src.policies.near_critical_policy import select_near_critical_interventions

def _arrays(nodes: pd.DataFrame):
    ops = nodes[nodes.node_type != "customer_region"].copy()
    # synthetic node-level lead times derived from layer type
    layer_map = {"supplier": 5.0, "factory": 4.0, "dc": 3.0, "warehouse": 2.0}
    lt_mean = ops.node_type.map(layer_map).fillna(3.0).to_numpy(dtype=np.float64)
    lt_std = np.maximum(0.5, lt_mean * 0.25)
    return (
        ops.capacity.to_numpy(dtype=np.float64),
        ops.demand_mean.to_numpy(dtype=np.float64),
        ops.failure_prob.to_numpy(dtype=np.float64),
        ops.initial_inventory.to_numpy(dtype=np.float64),
        ops.reorder_point.to_numpy(dtype=np.float64),
        ops.target_stock.to_numpy(dtype=np.float64),
        ops.holding_cost.to_numpy(dtype=np.float64),
        ops.backorder_cost.to_numpy(dtype=np.float64),
        ops.k_fail.to_numpy(dtype=np.float64),
        lt_mean.astype(np.float64),
        lt_std.astype(np.float64),
    )

def run_monte_carlo_v3(
    nodes: pd.DataFrame,
    scenarios: pd.DataFrame,
    days: int = 365,
    n_runs: int = 250,
    budget: float = 50000.0,
    seed: int = 42,
    max_pipeline_orders: int = 12,
    do_warmup: bool = True,
) -> pd.DataFrame:
    if do_warmup:
        print("    [numba] warming up v3 inventory kernel...")
        t0 = time.perf_counter()
        warmup_numba()
        print(f"    [numba] warm-up complete in {time.perf_counter() - t0:.2f}s")

    rows = []
    policies = ["no_intervention", "traditional", "near_critical"]
    total_jobs = len(scenarios) * len(policies)
    job = 0

    for _, scen in scenarios.iterrows():
        scenario = scen.to_dict()
        for policy in policies:
            job += 1
            print(f"    [{job}/{total_jobs}] scenario={scenario['scenario']} policy={policy} days={days} runs={n_runs}")
            t0 = time.perf_counter()

            if policy == "traditional":
                interventions = select_traditional_interventions(nodes, budget)
                sim_nodes = apply_interventions(nodes, interventions)
            elif policy == "near_critical":
                interventions = select_near_critical_interventions(nodes, budget)
                sim_nodes = apply_interventions(nodes, interventions)
            else:
                sim_nodes = nodes.copy()

            arrs = _arrays(sim_nodes)
            res = simulate_inventory_v3_numba(
                *arrs,
                float(scenario.get("demand_multiplier", 1.0)),
                float(scenario.get("failure_multiplier", 1.0)),
                float(scenario.get("lead_time_multiplier", 1.0)),
                int(days),
                int(n_runs),
                int(max_pipeline_orders),
                int(seed + job * 100000),
            )

            for i in range(n_runs):
                rows.append({
                    "scenario": scenario["scenario"],
                    "policy": policy,
                    "run": i,
                    "total_cost": float(res[0][i]),
                    "stockouts": float(res[1][i]),
                    "service_level": float(res[2][i]),
                    "collapse_events": float(res[3][i]),
                    "avg_backorders": float(res[4][i]),
                    "avg_inventory": float(res[5][i]),
                    "time_to_first_collapse": float(res[6][i]),
                })
            print(f"        completed in {time.perf_counter() - t0:.2f}s")
    return pd.DataFrame(rows)
