"""Style agent node: linting, naming, and formatting heuristics."""

from __future__ import annotations

import re
from typing import Any

from graph.state import CodeReviewState, Finding, findings_update


def style_agent(state: CodeReviewState) -> dict[str, Any]:
    """Generate style findings without relying on external linters."""

    code = state.get("code", "")
    findings: list[Finding] = []

    function_name = re.compile(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")

    for idx, line in enumerate(code.splitlines(), start=1):
        if len(line) > 100:
            findings.append(
                {
                    "category": "style",
                    "title": "Long line",
                    "description": "Line exceeds recommended 100 characters.",
                    "severity": "info",
                    "file": "in-memory.py",
                    "line": idx,
                    "confidence": 1.0,
                    "source": "style_agent",
                    "recommendation": "Wrap line to improve readability.",
                }
            )

        match = function_name.match(line.strip())
        if match and any(ch.isupper() for ch in match.group(1)):
            findings.append(
                {
                    "category": "style",
                    "title": "Non-snake_case function name",
                    "description": f"Function '{match.group(1)}' is not snake_case.",
                    "severity": "low",
                    "file": "in-memory.py",
                    "line": idx,
                    "confidence": 0.95,
                    "source": "style_agent",
                    "recommendation": "Rename function using snake_case naming.",
                }
            )

    return findings_update(state, "style_agent", findings)
