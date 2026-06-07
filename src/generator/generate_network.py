
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

def generate_nodes(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    specs = [
        ("supplier", 10, 250, 500, 0.03, 0.14),
        ("factory", 5, 400, 750, 0.02, 0.10),
        ("dc", 10, 250, 550, 0.02, 0.10),
        ("warehouse", 20, 120, 340, 0.03, 0.13),
        ("customer_region", 100, 20, 95, 0.0, 0.0),
    ]
    rows = []
    for node_type, n, cap_lo, cap_hi, p_lo, p_hi in specs:
        for i in range(n):
            node_id = f"{node_type[:3].upper()}_{i:03d}"
            capacity = float(rng.uniform(cap_lo, cap_hi))
            failure_prob = float(rng.uniform(p_lo, p_hi))
            if node_type == "customer_region":
                demand_mean = float(rng.uniform(cap_lo, cap_hi))
                init_inventory = 0.0
                reorder_point = 0.0
                target_stock = 0.0
            else:
                demand_mean = float(rng.uniform(0.65, 1.02) * capacity)
                init_inventory = float(rng.uniform(0.8, 1.4) * capacity)
                reorder_point = float(rng.uniform(0.35, 0.65) * capacity)
                target_stock = float(rng.uniform(1.0, 1.8) * capacity)
            rows.append({
                "node_id": node_id,
                "node_type": node_type,
                "capacity": capacity,
                "demand_mean": demand_mean,
                "failure_prob": failure_prob,
                "initial_inventory": init_inventory,
                "reorder_point": reorder_point,
                "target_stock": target_stock,
                "holding_cost": float(rng.uniform(0.05, 0.25)),
                "backorder_cost": float(rng.uniform(5, 25)),
                "k_fail": float(rng.uniform(5000, 60000)),
                "k_prevent": float(rng.uniform(500, 6000)),
                "x": float(rng.uniform(0, 100)),
                "y": float(rng.uniform(0, 100)),
            })
    return pd.DataFrame(rows)

def _connect_layers(rng, nodes, src_type, dst_type, min_links, max_links):
    src = nodes[nodes.node_type == src_type].node_id.to_list()
    dst = nodes[nodes.node_type == dst_type].node_id.to_list()
    rows = []
    for d in dst:
        k = int(rng.integers(min_links, max_links + 1))
        chosen = rng.choice(src, size=min(k, len(src)), replace=False)
        weights = rng.dirichlet(np.ones(len(chosen)))
        for s, w in zip(chosen, weights):
            rows.append({
                "from_node": s,
                "to_node": d,
                "supply_share": float(w),
                "transport_cost": float(rng.uniform(15, 220)),
                "lead_time_mean": float(rng.uniform(1, 8)),
                "lead_time_std": float(rng.uniform(0.2, 2.5)),
                "link_failure_prob": float(rng.uniform(0.005, 0.05)),
            })
    return rows

def generate_edges(nodes: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed + 1)
    rows = []
    rows += _connect_layers(rng, nodes, "supplier", "factory", 2, 4)
    rows += _connect_layers(rng, nodes, "factory", "dc", 1, 3)
    rows += _connect_layers(rng, nodes, "dc", "warehouse", 1, 3)
    rows += _connect_layers(rng, nodes, "warehouse", "customer_region", 1, 2)
    return pd.DataFrame(rows)

def generate_scenarios() -> pd.DataFrame:
    return pd.DataFrame([
        {"scenario": "baseline", "demand_multiplier": 1.00, "failure_multiplier": 1.00, "lead_time_multiplier": 1.00},
        {"scenario": "demand_shock_20", "demand_multiplier": 1.20, "failure_multiplier": 1.00, "lead_time_multiplier": 1.00},
        {"scenario": "leadtime_shock_50", "demand_multiplier": 1.00, "failure_multiplier": 1.00, "lead_time_multiplier": 1.50},
        {"scenario": "crisis_failures_2x", "demand_multiplier": 1.00, "failure_multiplier": 2.00, "lead_time_multiplier": 1.20},
        {"scenario": "near_critical", "demand_multiplier": 1.12, "failure_multiplier": 1.35, "lead_time_multiplier": 1.25},
    ])

def save_network(out_dir: str | Path = "data", seed: int = 42):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    nodes = generate_nodes(seed)
    edges = generate_edges(nodes, seed)
    scenarios = generate_scenarios()
    nodes.to_csv(out_dir / "nodes.csv", index=False)
    edges.to_csv(out_dir / "edges.csv", index=False)
    scenarios.to_csv(out_dir / "scenarios.csv", index=False)
    return nodes, edges, scenarios
