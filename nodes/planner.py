"""Planner node: decide review scope and decompose tasks."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState


def planner(state: CodeReviewState) -> dict[str, Any]:
    """Determine which analysis phases should run for this request."""

    language = state.get("language", "unknown")
    metadata = state.get("metadata", {})

    run_analysis = language in {"python", "javascript", "typescript"}
    run_security = True

    if language == "unknown" and not metadata.get("has_diff", False):
        run_analysis = False

    tasks = [
        "intake.complete",
        "analysis.ast_semantic_performance_style_docs" if run_analysis else "analysis.skipped",
        "security.vuln_dependency_research" if run_security else "security.skipped",
        "review.aggregate_validate_rank_fix_report",
    ]

    return {
        "task_flags": {
            "run_analysis": run_analysis,
            "run_security": run_security,
        },
        "tasks": tasks,
    }
