from __future__ import annotations

import math
import re
from collections.abc import Mapping
from dataclasses import dataclass
from numbers import Real


@dataclass(frozen=True)
class ReleaseDecision:
    approved: bool
    failures: tuple[str, ...]


def _is_finite_number(value: object) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(value)


def evaluate_release(
    *,
    metrics: Mapping[str, float],
    minimums: Mapping[str, float],
    artifact_sha256: str,
    dataset_version: str,
    model_version: str,
) -> ReleaseDecision:
    failures: list[str] = []

    if (
        not isinstance(artifact_sha256, str)
        or re.fullmatch(r"[0-9a-fA-F]{64}", artifact_sha256) is None
    ):
        failures.append("invalid_artifact_sha256")

    if not isinstance(dataset_version, str) or not dataset_version.strip():
        failures.append("missing_dataset_version")

    if not isinstance(model_version, str) or not model_version.strip():
        failures.append("missing_model_version")

    for metric, minimum in minimums.items():
        if not _is_finite_number(minimum):
            failures.append(f"invalid_threshold:{metric}")
            continue

        if metric not in metrics:
            failures.append(f"missing_metric:{metric}")
            continue

        observed = metrics[metric]
        if not _is_finite_number(observed):
            failures.append(f"invalid_metric:{metric}")
        elif observed < minimum:
            failures.append(f"threshold_failed:{metric}")

    return ReleaseDecision(not failures, tuple(failures))
