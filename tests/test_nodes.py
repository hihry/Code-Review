"""Tests for individual node behavior."""

from __future__ import annotations

from graph.state import new_state
from nodes.ast_analyzer import ast_analyzer
from nodes.intake import intake
from nodes.security_scanner import security_scanner


def test_intake_detects_python_and_parses_diff(sample_code: str, sample_patch: str) -> None:
    state = new_state(sample_code, language="auto", diff=sample_patch)
    update = intake(state)

    assert update["language"] == "python"
    assert update["metadata"]["has_diff"] is True
    assert len(update["parsed_diff"]) >= 1


def test_ast_analyzer_returns_summary(sample_code: str) -> None:
    state = new_state(sample_code, language="python")
    update = ast_analyzer(state)

    assert "ast_summary" in update
    assert "process_data" in update["ast_summary"]["functions"]


def test_security_scanner_flags_known_issues(sample_code: str) -> None:
    state = new_state(sample_code, language="python")
    update = security_scanner(state)

    findings = update["findings"]
    titles = {f["title"] for f in findings}
    assert "Dynamic code execution" in titles
    assert "Potential hardcoded secret (aws_access_key)" in titles
