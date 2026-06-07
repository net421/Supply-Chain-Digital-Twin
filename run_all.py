
from pathlib import Path
import argparse
import time

from src.generator.generate_network import save_network
from src.analytics.delta_metrics import add_near_critical_metrics
from src.analytics.network_criticality import compute_network_metrics
from src.analytics.kpis import summarize_simulation, compare_to_traditional
from src.simulation.monte_carlo import run_monte_carlo_v3
from src.optimization.intervention_engine import build_intervention_ranking
from src.reporting.plots import generate_plots
from src.reporting.executive_report import generate_report
from src.reporting.dashboard import generate_dashboard

def parse_args():
    p = argparse.ArgumentParser(description="Supply Chain Digital Twin v3")
    p.add_argument("--days", type=int, default=365)
    p.add_argument("--runs", type=int, default=250)
    p.add_argument("--budget", type=float, default=50000.0)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--fast", action="store_true", help="90 days / 25 runs")
    return p.parse_args()

def main():
    args = parse_args()
    days = 90 if args.fast else args.days
    runs = 25 if args.fast else args.runs

    for d in ["data","results","figures","reports"]:
        Path(d).mkdir(exist_ok=True)

    t0 = time.perf_counter()

    print("[1/7] Generating v3 synthetic supply-chain network...")
    nodes, edges, scenarios = save_network("data", seed=args.seed)

    print("[2/7] Computing near-critical metrics...")
    nodes = add_near_critical_metrics(nodes)

    print("[3/7] Computing network criticality...")
    nodes = compute_network_metrics(nodes, edges)
    nodes = add_near_critical_metrics(nodes)
    nodes.to_csv("data/nodes_enriched.csv", index=False)

    print("[4/7] Building intervention ranking...")
    ranking = build_intervention_ranking(nodes)
    ranking.to_csv("results/intervention_ranking.csv", index=False)

    print("[5/7] Running Numba v3 inventory digital twin...")
    sim = run_monte_carlo_v3(nodes, scenarios, days=days, n_runs=runs, budget=args.budget, seed=args.seed)
    sim.to_csv("results/monte_carlo_results.csv", index=False)

    print("[6/7] Summarizing policy comparison...")
    summary = summarize_simulation(sim)
    comparison = compare_to_traditional(summary)
    summary.to_csv("results/policy_summary.csv", index=False)
    comparison.to_csv("results/policy_comparison.csv", index=False)

    print("[7/7] Generating plots and reports...")
    generate_plots(nodes, ranking, comparison, "figures")
    generate_report(nodes, ranking, comparison, "reports/executive_report.md")
    generate_dashboard(nodes, ranking, comparison, "reports/dashboard.html")

    print("Done.")
    print(f"Total runtime: {time.perf_counter() - t0:.2f}s")
    print("Open: reports/dashboard.html")
    print("Read: reports/executive_report.md")

if __name__ == "__main__":
    main()
