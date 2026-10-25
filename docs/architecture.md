# Architecture: ml-experiment-release

The core logic is isolated in a small Python package. Inputs are validated at public boundaries; deterministic logic is covered by unit tests. The CI workflow runs formatting, linting, and tests on Python 3.13. External integrations are intentionally excluded from the default test path.
