"""Dependency auditor node: dependency risk and license heuristics."""

from __future__ import annotations

import re
from typing import Any

from graph.state import CodeReviewState, Finding, findings_update


def dependency_auditor(state: CodeReviewState) -> dict[str, Any]:
    """Check dependency declarations embedded in source/diff metadata."""

    code = state.get("code", "")
    findings: list[Finding] = []

    dep_patterns = [
        re.compile(r"^[\w\-]+\s*==\s*\d", re.MULTILINE),
        re.compile(r"^[\w\-]+\s*>=\s*\d", re.MULTILINE),
    ]

    dep_matches = 0
    for pattern in dep_patterns:
        dep_matches += len(pattern.findall(code))

    if dep_matches > 0:
        findings.append(
            {
                "category": "dependency",
                "title": "Dependency versions require audit",
                "description": "Detected inline dependency declarations; ensure versions are patched and licenses approved.",
                "severity": "medium",
                "file": "in-memory.py",
                "line": 1,
                "confidence": 0.65,
                "source": "dependency_auditor",
                "recommendation": "Run dependency scanners and review CVE advisories.",
            }
        )

    if state.get("metadata", {}).get("diff_files", 0) > 5:
        findings.append(
            {
                "category": "dependency",
                "title": "Large dependency-related change set",
                "description": "Wide patch sets often need deeper dependency and license verification.",
                "severity": "low",
                "file": "in-memory.py",
                "line": 1,
                "confidence": 0.55,
                "source": "dependency_auditor",
                "recommendation": "Verify transitive dependencies and lockfile consistency.",
            }
        )

    return findings_update(state, "dependency_auditor", findings)
