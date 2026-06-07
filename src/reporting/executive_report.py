
from __future__ import annotations
from pathlib import Path

def generate_report(nodes, ranking, comparison, out_path="reports/executive_report.md"):
    out_path = Path(out_path)
    out_path.parent.mkdir(exist_ok=True)
    top = ranking.iloc[0]
    nc = comparison[comparison.policy=="near_critical"]["cost_reduction_vs_traditional"].mean()
    txt = f"""# Supply Chain Digital Twin v3 — Executive Report

## What v3 Adds

This version includes dynamic inventory, reorder points, target stock, backorders, stochastic lead times, disruption shocks and Numba-optimized Monte Carlo.

## Main Recommendation

Top node to improve:

| Field | Value |
|---|---:|
| Node | {top['node_id']} |
| Type | {top['node_type']} |
| Delta | {top['delta']:.2f} |
| Utilization | {top['utilization']:.2%} |
| Fragility | {top['fragility']:.3f} |
| Network Criticality | {top['network_criticality']:.3f} |
| Resilience per Dollar | {top['resilience_per_dollar']:.6f} |

## Policy Result

Average near-critical cost reduction vs traditional:

**{nc:.2%}**

## Interpretation

The v3 engine does not only ask which node has high utilization. It asks which node combines:

```text
physical fragility + economic severity + network position
```

This is the operational translation of the Near-Critical Networks framework into a supply-chain digital twin.
"""
    out_path.write_text(txt, encoding="utf-8")
