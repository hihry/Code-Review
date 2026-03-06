"""AST analyzer node: parse tree, call graph, control flow metadata."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState, Finding, error_update, findings_update
from tools.ast_parser import parse_python_code


def ast_analyzer(state: CodeReviewState) -> dict[str, Any]:
    """Analyze source structure using language AST where available."""

    if state.get("language") != "python":
        return {}

    code = state.get("code", "")
    try:
        result = parse_python_code(code)
    except SyntaxError as exc:
        finding: Finding = {
            "category": "correctness",
            "title": "Syntax error",
            "description": str(exc),
            "severity": "high",
            "file": "in-memory.py",
            "line": int(getattr(exc, "lineno", 1) or 1),
            "confidence": 1.0,
            "source": "ast_analyzer",
            "recommendation": "Fix syntax errors before running static analysis.",
        }
        update = findings_update(state, "ast_analyzer", [finding])
        update.update(error_update(state, f"AST parse failed: {exc}"))
        return update

    return {
        "ast_summary": result["summary"],
        "call_graph": result["call_graph"],
        "control_flow": result["control_flow"],
    }
