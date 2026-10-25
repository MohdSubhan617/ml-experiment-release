# ML Experiment Release

A small release gate that compares caller-supplied metrics to minimum thresholds and checks release metadata fields.

## Usage

```python
from ml_experiment_release.release import evaluate_release

decision = evaluate_release(
    metrics={"auc": 0.91},
    minimums={"auc": 0.90},
    artifact_sha256="a" * 64,
    dataset_version="dataset-v2",
    model_version="model-v1",
)
assert decision.approved
```

A missing or non-finite metric, invalid threshold, below-threshold value, malformed 64-character hexadecimal digest, or blank version fails closed with a reason code. The digest is checked for format only: this function does not hash an artifact, verify provenance, persist an approval, or authenticate the supplied metrics. It is a policy primitive, not a complete model registry or release system.

## Setup and checks

Requires Python 3.13 or newer. Runtime has no third-party dependencies.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pip check
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m pip_audit --local --skip-editable --progress-spinner off --timeout 60
```

Thresholds should be chosen and versioned by the consuming release process. This repository publishes no model-quality benchmark claims.
