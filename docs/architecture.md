# Architecture: ml-experiment-release

`evaluate_release` compares each configured minimum with the corresponding supplied metric, reports missing or invalid values, validates the digest's hexadecimal length and version strings, and returns `ReleaseDecision(approved, failures)`. Metric and threshold values must be finite real numbers; booleans are rejected as numbers.

The function evaluates metadata claims but does not read the model artifact, calculate its digest, load a dataset, or authenticate measured metrics. It is a deterministic policy component for a larger release workflow.
