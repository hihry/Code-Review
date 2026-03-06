"""Ranker node: severity scoring and prioritization."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState, Finding


SEVERITY_WEIGHTS = {
    "critical": 10,
    "high": 7,
    "medium": 4,
    "low": 2,
    "info": 1,
}


def ranker(state: CodeReviewState) -> dict[str, Any]:
    """Sort validated findings by severity and confidence."""

    findings = list(state.get("validated_findings", []))
    findings.sort(
        key=lambda f: (
            SEVERITY_WEIGHTS.get(str(f.get("severity", "info")), 0),
            float(f.get("confidence", 0.0) or 0.0),
        ),
        reverse=True,
    )

    total_weight = sum(SEVERITY_WEIGHTS.get(str(f.get("severity", "info")), 0) for f in findings)
    score = max(0.0, 100.0 - float(total_weight * 2))

    return {
        "ranked_findings": findings,
        "overall_score": round(score, 2),
    }
