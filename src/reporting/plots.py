
from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def save_hbar(df, label, value, title, path, top=20):
    d = df[[label, value]].dropna().sort_values(value, ascending=False).head(top)
    plt.figure(figsize=(10, 6))
    plt.barh(d[label].astype(str), d[value])
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.xlabel(value.replace("_", " ").title())
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()

def generate_plots(nodes, ranking, comparison, out_dir="figures"):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    save_hbar(ranking, "node_id", "resilience_per_dollar", "Top Nodes by Resilience per Dollar", out_dir/"resilience_per_dollar.png")
    save_hbar(nodes[nodes.node_type!="customer_region"], "node_id", "fragility", "Near-Critical Fragility by Node", out_dir/"fragility.png")
    save_hbar(nodes[nodes.node_type!="customer_region"], "node_id", "network_criticality", "Network Criticality by Node", out_dir/"network_criticality.png")
    pivot = comparison.pivot(index="scenario", columns="policy", values="total_cost")
    pivot.plot(kind="bar", figsize=(11,6))
    plt.title("Expected Total Cost by Scenario and Policy")
    plt.ylabel("Expected Total Cost")
    plt.tight_layout()
    plt.savefig(out_dir/"policy_cost_comparison.png", dpi=160, bbox_inches="tight")
    plt.close()
    pivot2 = comparison.pivot(index="scenario", columns="policy", values="service_level")
    pivot2.plot(kind="bar", figsize=(11,6))
    plt.title("Service Level by Scenario and Policy")
    plt.ylabel("Service Level")
    plt.tight_layout()
    plt.savefig(out_dir/"service_level_comparison.png", dpi=160, bbox_inches="tight")
    plt.close()
