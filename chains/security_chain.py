"""Security chain: scanner -> dependency audit -> research enrichment."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState
from nodes.dependency_auditor import dependency_auditor
from nodes.research_agent import research_agent
from nodes.security_scanner import security_scanner


def _apply_update(state: CodeReviewState, update: dict[str, Any]) -> CodeReviewState:
    merged = dict(state)
    merged.update(update)
    return CodeReviewState(**merged)


def run_security_chain(state: CodeReviewState) -> dict[str, Any]:
    """Execute all security-focused reviewer nodes in order."""

    current = state
    for node in [security_scanner, dependency_auditor, research_agent]:
        update = node(current)
        current = _apply_update(current, update)

    return dict(current)
