
from __future__ import annotations
import pandas as pd
import networkx as nx

def compute_network_metrics(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    G = nx.DiGraph()
    for _, r in edges.iterrows():
        G.add_edge(r["from_node"], r["to_node"], weight=float(r.get("supply_share", 1.0)))
    deg = nx.degree_centrality(G)
    btw = nx.betweenness_centrality(G, normalized=True)
    pr = nx.pagerank(G, alpha=0.85)
    out = nodes.copy()
    out["degree_centrality"] = out["node_id"].map(deg).fillna(0.0)
    out["betweenness"] = out["node_id"].map(btw).fillna(0.0)
    out["pagerank"] = out["node_id"].map(pr).fillna(0.0)
    out["network_criticality"] = (
        0.35 * out["degree_centrality"].rank(pct=True)
        + 0.45 * out["betweenness"].rank(pct=True)
        + 0.20 * out["pagerank"].rank(pct=True)
    )
    return out
