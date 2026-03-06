"""Performance analyzer node: complexity and scalability heuristics."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState, Finding, findings_update
from tools.complexity import calculate_complexity


def performance_analyzer(state: CodeReviewState) -> dict[str, Any]:
    """Detect performance risks like high complexity and nested loops."""

    if state.get("language") != "python":
        return {}

    code = state.get("code", "")
    complexity = calculate_complexity(code)
    findings: list[Finding] = []

    if complexity["cyclomatic"] >= 15:
        findings.append(
            {
                "category": "performance",
                "title": "High cyclomatic complexity",
                "description": f"Cyclomatic complexity is {complexity['cyclomatic']}.",
                "severity": "medium",
                "file": "in-memory.py",
                "line": 1,
                "confidence": 0.8,
                "source": "performance_analyzer",
                "recommendation": "Refactor into smaller functions and reduce branching.",
            }
        )

    nested_loops = 0
    for line in code.splitlines():
        if line.startswith("    for ") or line.startswith("    while "):
            nested_loops += 1
    if nested_loops >= 2:
        findings.append(
            {
                "category": "performance",
                "title": "Potential nested-loop hotspot",
                "description": "Nested loops may result in O(n^2) behavior for larger inputs.",
                "severity": "low",
                "file": "in-memory.py",
                "line": 1,
                "confidence": 0.6,
                "source": "performance_analyzer",
                "recommendation": "Consider indexing, caching, or algorithmic redesign.",
            }
        )

    update = findings_update(state, "performance_analyzer", findings)
    update["complexity"] = complexity
    return update
