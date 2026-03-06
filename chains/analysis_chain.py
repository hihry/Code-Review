"""Analysis chain: ast -> semantic -> performance -> style -> docs."""

from __future__ import annotations

from typing import Any, Callable

from graph.state import CodeReviewState
from nodes.ast_analyzer import ast_analyzer
from nodes.docs_agent import docs_agent
from nodes.performance_analyzer import performance_analyzer
from nodes.semantic_analyzer import semantic_analyzer
from nodes.style_agent import style_agent


NodeFunc = Callable[[CodeReviewState], dict[str, Any]]


def _apply_update(state: CodeReviewState, update: dict[str, Any]) -> CodeReviewState:
    merged = dict(state)
    merged.update(update)
    return CodeReviewState(**merged)


def run_analysis_chain(state: CodeReviewState) -> dict[str, Any]:
    """Execute the non-security analyzers sequentially."""

    current = state
    for node in [ast_analyzer, semantic_analyzer, performance_analyzer, style_agent, docs_agent]:
        update = node(current)
        current = _apply_update(current, update)

    return dict(current)
