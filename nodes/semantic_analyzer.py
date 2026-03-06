"""Semantic analyzer node: logic correctness and side-effect checks."""

from __future__ import annotations

import re
from typing import Any

from graph.state import CodeReviewState, Finding, findings_update


def semantic_analyzer(state: CodeReviewState) -> dict[str, Any]:
    """Run lightweight semantic heuristics over source text."""

    code = state.get("code", "")
    lines = code.splitlines()
    findings: list[Finding] = []

    mutable_default = re.compile(r"def\s+\w+\(.*=\s*(\[\]|\{\})")

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("except:"):
            findings.append(
                {
                    "category": "correctness",
                    "title": "Bare except clause",
                    "description": "Bare except swallows unexpected exceptions and hides bugs.",
                    "severity": "medium",
                    "file": "in-memory.py",
                    "line": idx,
                    "confidence": 0.95,
                    "source": "semantic_analyzer",
                    "recommendation": "Catch specific exception types.",
                }
            )
        if mutable_default.search(stripped):
            findings.append(
                {
                    "category": "correctness",
                    "title": "Mutable default argument",
                    "description": "Mutable defaults are shared between function calls.",
                    "severity": "medium",
                    "file": "in-memory.py",
                    "line": idx,
                    "confidence": 0.9,
                    "source": "semantic_analyzer",
                    "recommendation": "Use None and initialize inside the function.",
                }
            )

    return findings_update(state, "semantic_analyzer", findings)
