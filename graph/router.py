"""Conditional routing logic for the review graph."""

from __future__ import annotations

from typing import Literal

from .state import CodeReviewState


PlannerRoute = Literal["analysis", "security", "review"]
AnalysisRoute = Literal["security", "review"]


def route_after_planner(state: CodeReviewState) -> PlannerRoute:
    """Choose the next stage immediately after planning."""

    flags = state.get("task_flags", {})
    if flags.get("run_analysis", False):
        return "analysis"
    if flags.get("run_security", False):
        return "security"
    return "review"


def route_after_analysis(state: CodeReviewState) -> AnalysisRoute:
    """Run security stage when enabled, otherwise jump to review chain."""

    if state.get("task_flags", {}).get("run_security", False):
        return "security"
    return "review"
