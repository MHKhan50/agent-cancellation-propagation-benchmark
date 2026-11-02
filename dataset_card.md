# Dataset Card: ACPB Synthetic Cancellation Scenarios
- Version: 0.1.0; default records: 6,000; format: CSV.
- Seeds: 11, 23, 37, 51, 73.
- Fields: scenario_id, seed, workflow_depth, cancel_after_step, in_flight_calls, side_effect_step, failure_mode.
- Synthetic generator only; no personal or production data.
- Intended for reproducibility and metric prototyping; not for real-world incident-rate estimation or safety guarantees.
- Limitation: stylized model without real concurrency, network timing, rollback, or runtime integration.
