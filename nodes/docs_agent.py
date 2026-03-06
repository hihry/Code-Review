"""Documentation agent node: docstring and annotation checks."""

from __future__ import annotations

import ast
from typing import Any

from graph.state import CodeReviewState, Finding, findings_update


def docs_agent(state: CodeReviewState) -> dict[str, Any]:
    """Identify missing docstrings and type annotations."""

    if state.get("language") != "python":
        return {}

    code = state.get("code", "")
    findings: list[Finding] = []

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {}

    if ast.get_docstring(tree) is None:
        findings.append(
            {
                "category": "documentation",
                "title": "Missing module docstring",
                "description": "Module-level docstring is absent.",
                "severity": "info",
                "file": "in-memory.py",
                "line": 1,
                "confidence": 1.0,
                "source": "docs_agent",
                "recommendation": "Add a short module docstring describing purpose.",
            }
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if ast.get_docstring(node) is None:
                findings.append(
                    {
                        "category": "documentation",
                        "title": "Missing function docstring",
                        "description": f"Function '{node.name}' lacks a docstring.",
                        "severity": "low",
                        "file": "in-memory.py",
                        "line": node.lineno,
                        "confidence": 1.0,
                        "source": "docs_agent",
                        "recommendation": "Document parameters, return value, and side effects.",
                    }
                )
            if node.returns is None:
                findings.append(
                    {
                        "category": "documentation",
                        "title": "Missing return type annotation",
                        "description": f"Function '{node.name}' has no return type annotation.",
                        "severity": "info",
                        "file": "in-memory.py",
                        "line": node.lineno,
                        "confidence": 0.9,
                        "source": "docs_agent",
                        "recommendation": "Add explicit return type hints.",
                    }
                )

    return findings_update(state, "docs_agent", findings)
