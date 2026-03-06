"""Validator node: reduce false positives and verify locations."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState, Finding


def validator(state: CodeReviewState) -> dict[str, Any]:
    """Filter findings by confidence and valid line numbers."""

    line_count = len(state.get("code", "").splitlines())
    validated: list[Finding] = []

    for finding in state.get("findings", []):
        confidence = float(finding.get("confidence", 0.0) or 0.0)
        line = int(finding.get("line", 0) or 0)
        if confidence < 0.5:
            continue
        if line_count > 0 and (line <= 0 or line > line_count):
            continue
        validated.append(finding)

    return {"validated_findings": validated}
