# Supply Chain Digital Twin v3 — Executive Report

## What v3 Adds

This version includes dynamic inventory, reorder points, target stock, backorders, stochastic lead times, disruption shocks and Numba-optimized Monte Carlo.

## Main Recommendation

Top node to improve:

| Field | Value |
|---|---:|
| Node | WAR_012 |
| Type | warehouse |
| Delta | -20.41 |
| Utilization | 101.27% |
| Fragility | 1.000 |
| Network Criticality | 0.871 |
| Resilience per Dollar | 0.039061 |

## Policy Result

Average near-critical cost reduction vs traditional:

**0.11%**

## Interpretation

The v3 engine does not only ask which node has high utilization. It asks which node combines:

```text
physical fragility + economic severity + network position
```

This is the operational translation of the Near-Critical Networks framework into a supply-chain digital twin.
