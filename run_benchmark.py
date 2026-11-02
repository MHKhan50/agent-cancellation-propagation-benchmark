"""Run the default benchmark and write data/ and outputs/."""
from __future__ import annotations

import json
from pathlib import Path

from benchmark import evaluate, generate_scenarios, summarize, write_csv

ROOT = Path(__file__).resolve().parent


def main() -> None:
    scenarios = generate_scenarios()
    results = evaluate(scenarios)
    summary = summarize(results)
    write_csv(ROOT / "data" / "scenarios.csv", scenarios)
    write_csv(ROOT / "outputs" / "episode_results.csv", results)
    write_csv(ROOT / "outputs" / "policy_summary.csv", summary)
    payload = {
        "benchmark": "Agent Cancellation Propagation Benchmark",
        "version": "0.1.1",
        "synthetic_scenarios": len(scenarios),
        "policies": [x["policy"] for x in summary],
        "episodes_evaluated": len(results),
        "metrics": summary,
        "interpretation_warning": "Synthetic simulator results only; not measurements of deployed agents.",
    }
    text = json.dumps(payload, indent=2)
    (ROOT / "outputs" / "summary.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
