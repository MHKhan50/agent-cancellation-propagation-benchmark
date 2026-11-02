# Agent Cancellation Propagation Benchmark (ACPB)

**Version:** 0.1.0 | **Research date:** 1 November 2026 | **Author:** Muzammal Hussain

## Research question
When cancellation reaches a multi-step agent workflow, how do policies affect post-cancellation tool dispatches, orphaned calls, cancellation latency, and side effects?

## Policies
- `cooperative`: stops new dispatches immediately in this simplified model.
- `polling`: checks cancellation periodically and may permit limited residual work.
- `cancellation_blind`: continues the remaining workflow.
- `shielded_section`: completes a modeled protected section before observing cancellation.

## Run on macOS
```bash
python3 run_benchmark.py
python3 -m unittest discover -s tests -v
```
Default run: 6,000 synthetic scenarios, four policies, 24,000 policy-episode rows. Outputs: `data/scenarios.csv`, `outputs/episode_results.csv`, `outputs/policy_summary.csv`, `outputs/summary.json`.

## Limitations
Stylized deterministic simulator only; it does not model real concurrency, cancellation races, network timing, rollback, or framework-specific semantics. Do not present results as production measurements or safety guarantees.
