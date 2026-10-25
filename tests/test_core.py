import math

import pytest

from ml_experiment_release.release import evaluate_release


def evaluate(metrics: dict[str, float], minimums: dict[str, float]):
    return evaluate_release(
        metrics=metrics,
        minimums=minimums,
        artifact_sha256="a" * 64,
        dataset_version="ds-v2",
        model_version="model-v1",
    )


def test_release_passes_when_metadata_and_thresholds_pass():
    assert evaluate({"auc": 0.91}, {"auc": 0.9}).approved


def test_release_fails_on_missing_metric_and_bad_hash():
    result = evaluate_release(
        metrics={},
        minimums={"auc": 0.9},
        artifact_sha256="bad",
        dataset_version="d1",
        model_version="m1",
    )
    assert not result.approved
    assert "invalid_artifact_sha256" in result.failures
    assert "missing_metric:auc" in result.failures


def test_release_fails_below_threshold():
    result = evaluate({"auc": 0.7}, {"auc": 0.9})
    assert not result.approved
    assert "threshold_failed:auc" in result.failures


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_non_finite_metrics_fail_closed(value):
    result = evaluate({"auc": value}, {"auc": 0.9})
    assert not result.approved
    assert "invalid_metric:auc" in result.failures


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_non_finite_thresholds_fail_closed(value):
    result = evaluate({"auc": 0.95}, {"auc": value})
    assert not result.approved
    assert "invalid_threshold:auc" in result.failures


@pytest.mark.parametrize("value", [True, "0.95", None])
def test_non_numeric_metrics_fail_closed(value):
    result = evaluate({"auc": value}, {"auc": 0.9})
    assert not result.approved
    assert "invalid_metric:auc" in result.failures


@pytest.mark.parametrize("value", [True, "0.9", None])
def test_non_numeric_thresholds_fail_closed(value):
    result = evaluate({"auc": 0.95}, {"auc": value})
    assert not result.approved
    assert "invalid_threshold:auc" in result.failures


@pytest.mark.parametrize("field", ["dataset_version", "model_version"])
def test_blank_version_metadata_fails(field):
    kwargs = {
        "metrics": {"auc": 0.95},
        "minimums": {"auc": 0.9},
        "artifact_sha256": "a" * 64,
        "dataset_version": "ds-v2",
        "model_version": "model-v1",
    }
    kwargs[field] = " "
    result = evaluate_release(**kwargs)
    assert not result.approved
    assert f"missing_{field}" in result.failures


@pytest.mark.parametrize("digest", ["g" * 64, "A" * 63, ""])
def test_malformed_digest_fails(digest):
    result = evaluate_release(
        metrics={"auc": 0.95},
        minimums={"auc": 0.9},
        artifact_sha256=digest,
        dataset_version="ds-v2",
        model_version="model-v1",
    )
    assert not result.approved
    assert "invalid_artifact_sha256" in result.failures
