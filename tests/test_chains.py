"""Tests for chain and end-to-end execution."""

from __future__ import annotations

from main import run_review


def test_run_review_produces_report_and_ranked_findings(sample_code: str, sample_patch: str) -> None:
    result = run_review(sample_code, language="python", diff=sample_patch)

    assert result["report_markdown"].startswith("# Code Review Report")
    assert len(result["ranked_findings"]) > 0
    assert 0 <= result["overall_score"] <= 100
