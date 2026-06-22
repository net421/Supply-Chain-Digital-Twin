# Near-Critical Research Lineage

This document explains how the Supply Chain Digital Twin relates to the separate near-critical systems research line.

## Source concept

The earlier near-critical benchmark studied a controlled stochastic inventory/buffer system close to a stability boundary. Its key variables were:

- `delta`: stability margin, interpreted as expected supply minus expected demand.
- `K_fail / K_prevent`: collapse-to-prevention cost ratio.
- Preventive threshold control: intervene before collapse rather than waiting for run-to-failure.
- Monte Carlo policy comparison against run-to-failure and static safety policies.

## What the digital twin reuses

The digital twin reuses the near-critical idea that operational risk is not captured by average performance alone. A node can look acceptable under ordinary KPIs while operating close to a boundary where small shocks produce large losses.

The reused mechanisms are:

1. Stability-margin logic.
2. Preventive threshold policy comparison.
3. Physical/economic boundary interpretation.
4. Simulation-driven validation under stochastic demand and disruptions.

## What the digital twin adds

The digital twin translates the single-node logic into a networked supply-chain setting:

- Suppliers, factories, distribution centers, warehouses, and customers.
- Node-level and network-level stockout/lost-demand evaluation.
- Network-aware threshold policy.
- Delta-controlled demand scaling.
- Policy surfaces over physical criticality and economic severity.

## Optimized decision

The optimized decision is the preventive intervention threshold. The platform compares:

| Policy | Meaning |
|---|---|
| `run_to_failure` | No preventive control. |
| `static_safety` | Fixed safety-stock-like threshold. |
| `near_critical_local` | Threshold adapts to local stability margin. |
| `network_aware` | Local near-critical threshold adjusted by network relevance. |

## Working research claim

Preventive intervention value appears strongest when three dimensions reinforce one another:

1. Physical criticality: low stability margin.
2. Economic criticality: high failure/prevention cost ratio.
3. Network criticality: concentration of near-critical nodes or structurally important nodes.

The associated standalone research package should be published as:

`https://github.com/net421/near-critical-network-digital-twin`
