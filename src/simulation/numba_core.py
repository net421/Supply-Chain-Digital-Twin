
from __future__ import annotations
import numpy as np
from numba import njit

@njit(cache=True)
def simulate_inventory_v3_numba(
    capacity,
    demand_mean,
    failure_prob,
    initial_inventory,
    reorder_point,
    target_stock,
    holding_cost,
    backorder_cost,
    k_fail,
    lead_time_mean,
    lead_time_std,
    scenario_demand_multiplier,
    scenario_failure_multiplier,
    scenario_lead_time_multiplier,
    days,
    n_runs,
    max_pipeline_orders,
    seed,
):
    n = capacity.shape[0]

    total_costs = np.zeros(n_runs)
    stockouts_arr = np.zeros(n_runs)
    service_arr = np.zeros(n_runs)
    collapse_arr = np.zeros(n_runs)
    backorders_arr = np.zeros(n_runs)
    inventory_arr = np.zeros(n_runs)
    ttc_arr = np.zeros(n_runs)

    for run in range(n_runs):
        np.random.seed(seed + run)

        inv = initial_inventory.copy()
        back = np.zeros(n)

        # Simple pipeline arrays: quantity and days remaining
        pipe_qty = np.zeros((n, max_pipeline_orders))
        pipe_days = np.zeros((n, max_pipeline_orders))

        total_cost = 0.0
        stockouts = 0.0
        collapse_events = 0.0
        requested = 0.0
        fulfilled = 0.0
        inv_sum = 0.0
        back_sum = 0.0
        first_collapse = -1.0

        for day in range(days):
            # receive pipeline
            for j in range(n):
                for q in range(max_pipeline_orders):
                    if pipe_qty[j, q] > 0.0:
                        pipe_days[j, q] -= 1.0
                        if pipe_days[j, q] <= 0.0:
                            inv[j] += pipe_qty[j, q]
                            pipe_qty[j, q] = 0.0
                            pipe_days[j, q] = 0.0

            for j in range(n):
                lam = demand_mean[j] * scenario_demand_multiplier
                if lam < 0.01:
                    lam = 0.01

                demand = np.random.poisson(lam)
                requested += demand

                fp = failure_prob[j] * scenario_failure_multiplier
                if fp > 0.95:
                    fp = 0.95

                failed = np.random.random() < fp
                cap_today = 0.0 if failed else capacity[j]

                available = inv[j]
                if available > cap_today:
                    available = cap_today

                total_need = demand + back[j]
                shipped = available if available < total_need else total_need
                inv[j] -= shipped
                if inv[j] < 0.0:
                    inv[j] = 0.0

                fulfilled += shipped
                unmet = total_need - shipped
                if unmet < 0.0:
                    unmet = 0.0
                back[j] = unmet

                if unmet > 0.0:
                    stockouts += 1.0
                    total_cost += unmet * backorder_cost[j]
                    if total_need > 0.0 and unmet > 0.50 * total_need:
                        collapse_events += 1.0
                        total_cost += k_fail[j] * 0.05
                        if first_collapse < 0.0:
                            first_collapse = day + 1.0

                if failed:
                    total_cost += k_fail[j] * 0.01

                total_cost += inv[j] * holding_cost[j]

                # reorder rule
                if inv[j] <= reorder_point[j]:
                    outstanding = 0.0
                    empty_slot = -1
                    for q in range(max_pipeline_orders):
                        outstanding += pipe_qty[j, q]
                        if empty_slot < 0 and pipe_qty[j, q] <= 0.0:
                            empty_slot = q
                    order_qty = target_stock[j] - inv[j] - outstanding
                    if order_qty > 0.0 and empty_slot >= 0:
                        lt = np.random.normal(lead_time_mean[j] * scenario_lead_time_multiplier, lead_time_std[j])
                        if lt < 1.0:
                            lt = 1.0
                        pipe_qty[j, empty_slot] = order_qty
                        pipe_days[j, empty_slot] = np.ceil(lt)

                inv_sum += inv[j]
                back_sum += back[j]

        total_costs[run] = total_cost
        stockouts_arr[run] = stockouts
        service_arr[run] = fulfilled / requested if requested > 0.0 else 1.0
        collapse_arr[run] = collapse_events
        backorders_arr[run] = back_sum / (days * n)
        inventory_arr[run] = inv_sum / (days * n)
        ttc_arr[run] = first_collapse if first_collapse > 0.0 else days + 1.0

    return total_costs, stockouts_arr, service_arr, collapse_arr, backorders_arr, inventory_arr, ttc_arr


def warmup_numba():
    capacity = np.array([100.0, 120.0])
    demand_mean = np.array([80.0, 95.0])
    failure_prob = np.array([0.05, 0.08])
    initial_inventory = np.array([120.0, 140.0])
    reorder_point = np.array([50.0, 60.0])
    target_stock = np.array([160.0, 180.0])
    holding_cost = np.array([0.1, 0.1])
    backorder_cost = np.array([10.0, 12.0])
    k_fail = np.array([10000.0, 12000.0])
    lead_time_mean = np.array([3.0, 4.0])
    lead_time_std = np.array([1.0, 1.0])
    simulate_inventory_v3_numba(
        capacity, demand_mean, failure_prob, initial_inventory,
        reorder_point, target_stock, holding_cost, backorder_cost, k_fail,
        lead_time_mean, lead_time_std,
        1.0, 1.0, 1.0,
        2, 2, 8, 123
    )
