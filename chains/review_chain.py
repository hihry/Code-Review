"""Review chain: aggregate -> validate -> rank -> fix -> report."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState
from nodes.aggregator import aggregator
from nodes.fix_suggester import fix_suggester
from nodes.ranker import ranker
from nodes.report_generator import report_generator
from nodes.validator import validator


def _apply_update(state: CodeReviewState, update: dict[str, Any]) -> CodeReviewState:
    merged = dict(state)
    merged.update(update)
    return CodeReviewState(**merged)


def run_review_chain(state: CodeReviewState) -> dict[str, Any]:
    """Execute post-analysis review processing nodes in sequence."""

    current = state
    for node in [aggregator, validator, ranker, fix_suggester, report_generator]:
        update = node(current)
        current = _apply_update(current, update)

    return dict(current)
