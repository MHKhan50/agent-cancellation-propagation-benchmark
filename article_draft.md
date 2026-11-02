# Agent Cancellation Propagation Benchmark: Measuring Work That Continues After an Agent Is Told to Stop

**Author:** Muzammal Hussain | **Date:** 1 November 2026 | **Version:** ACPB v0.1.0

## Abstract
Cancellation is a control signal, but its arrival does not necessarily mean downstream work has stopped. This benchmark provides a deterministic synthetic testbed for measuring post-cancellation tool dispatches, orphaned calls, cancellation latency, and side effects. Four stylized policies are evaluated over seeded workflow scenarios. This is a reproducible measurement baseline, not an empirical claim about deployed agents.

## Method
The default run generates 6,000 synthetic scenarios using five fixed seeds. Workflow depth, cancellation point, in-flight calls, possible side-effect location, and cancellation source vary. Each scenario is evaluated under cooperative, polling, cancellation-blind, and shielded-section policies, yielding 24,000 policy-episode records.

## Measures
Post-cancellation dispatches, orphaned calls, simulated cancellation latency, post-cancellation side-effect occurrence, and a strict compliance indicator.

## Limitations
All outcomes follow explicit simulator rules. They are not estimates of real-world agent behavior. The model omits real concurrency, cancellation races, network partitions, rollback, and framework-specific semantics. Runtime adapters and trace-based experiments are needed before making claims about real systems.
