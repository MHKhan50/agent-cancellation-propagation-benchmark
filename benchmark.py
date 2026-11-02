"""Synthetic benchmark for cancellation propagation in agent workflows.

Each scenario is a workflow of `workflow_depth` steps. Cancellation arrives after
`cancel_after_step`, while `in_flight_calls` tool calls are still running. A side
effect (for example a sent message) is scheduled at `side_effect_step`.

Each policy is a fixed rule, so the policy numbers in the outputs follow directly
from these rules and the scenario mix. The value of the benchmark is in making
those rules explicit and comparable, not in discovering behaviour.
"""
from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

POLICIES = ("cooperative", "polling", "cancellation_blind", "shielded_section")
FAILURE_MODES = ("user_cancel", "parent_timeout", "budget_exhausted")

Row = Dict[str, object]


def generate_scenarios(n: int = 1200, seeds: Sequence[int] = (11, 23, 37, 51, 73)) -> List[Row]:
    """Generate `n` scenarios per seed. The same seeds always give the same rows."""
    rows: List[Row] = []
    for seed in seeds:
        rng = random.Random(seed)
        for i in range(n):
            depth = rng.randint(2, 6)
            rows.append({
                "scenario_id": f"s{seed}_{i:05d}",
                "seed": seed,
                "workflow_depth": depth,
                "cancel_after_step": rng.randint(1, depth - 1),
                "in_flight_calls": rng.randint(0, 3),
                "side_effect_step": rng.choice([0, 1, 2, 3]),
                "failure_mode": rng.choice(FAILURE_MODES),
            })
    return rows


def simulate(row: Row, policy: str) -> Row:
    """Apply one policy rule to one scenario."""
    depth = int(row["workflow_depth"])
    cancel = int(row["cancel_after_step"])
    inflight = int(row["in_flight_calls"])
    side = int(row["side_effect_step"])
    # A side effect can happen after cancellation only if it is scheduled later in the workflow.
    possible = int(cancel < side <= depth)

    if policy == "cooperative":
        # Stops new dispatches at once; a running call can still finish its effect.
        dispatch, orphan, latency, effects = 0, 0, 1, int(possible and inflight > 0)
    elif policy == "polling":
        # Notices the stop at the next poll, so one more call may go out.
        dispatch, orphan, latency, effects = min(1, depth - cancel), min(inflight, 1), 2, int(possible and inflight >= 2)
    elif policy == "cancellation_blind":
        # Ignores the stop and runs the rest of the workflow.
        dispatch, orphan, latency, effects = depth - cancel, inflight, depth - cancel + 2, possible
    elif policy == "shielded_section":
        # Finishes a protected section (which holds the side effect) before stopping.
        dispatch, orphan, latency, effects = possible, max(0, inflight - 1), 2 + possible, possible
    else:
        raise ValueError(f"Unknown policy: {policy}")

    return {
        "policy": policy,
        "post_cancel_dispatches": dispatch,
        "orphaned_calls": orphan,
        "cancel_latency_steps": latency,
        "post_cancel_side_effects": effects,
        "cancel_compliance": int(dispatch == 0 and effects == 0),
    }


def evaluate(rows: Iterable[Row]) -> List[Row]:
    """Run every policy on every scenario (paired design)."""
    return [{**r, **simulate(r, p)} for r in rows for p in POLICIES]


def _mean(rows: List[Row], key: str) -> float:
    return round(sum(float(x[key]) for x in rows) / len(rows), 4)


def summarize(results: List[Row]) -> List[Row]:
    """Per-policy means and rates."""
    out: List[Row] = []
    for p in POLICIES:
        s = [r for r in results if r["policy"] == p]
        out.append({
            "policy": p,
            "episodes": len(s),
            "mean_post_cancel_dispatches": _mean(s, "post_cancel_dispatches"),
            "mean_orphaned_calls": _mean(s, "orphaned_calls"),
            "mean_cancel_latency_steps": _mean(s, "cancel_latency_steps"),
            "post_cancel_side_effect_rate": _mean(s, "post_cancel_side_effects"),
            "cancel_compliance_rate": _mean(s, "cancel_compliance"),
        })
    return out


def write_csv(path: Path, rows: List[Row]) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
