"""Security scanner node: OWASP-style heuristics and secret detection."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState, Finding, findings_update
from tools.secret_scanner import find_potential_secrets


def security_scanner(state: CodeReviewState) -> dict[str, Any]:
    """Inspect code for common security risks and hardcoded secrets."""

    code = state.get("code", "")
    findings: list[Finding] = []

    for secret in find_potential_secrets(code):
        findings.append(
            {
                **secret,
                "source": "security_scanner",
            }
        )

    for idx, line in enumerate(code.splitlines(), start=1):
        stripped = line.strip()
        if "eval(" in stripped or "exec(" in stripped:
            findings.append(
                {
                    "category": "security",
                    "title": "Dynamic code execution",
                    "description": "Using eval/exec can lead to code injection vulnerabilities.",
                    "severity": "high",
                    "file": "in-memory.py",
                    "line": idx,
                    "confidence": 0.9,
                    "source": "security_scanner",
                    "recommendation": "Use safe parsing or explicit dispatch logic.",
                }
            )
        if "subprocess" in stripped and "shell=True" in stripped:
            findings.append(
                {
                    "category": "security",
                    "title": "Shell injection risk",
                    "description": "subprocess with shell=True can expose shell injection attack paths.",
                    "severity": "high",
                    "file": "in-memory.py",
                    "line": idx,
                    "confidence": 0.85,
                    "source": "security_scanner",
                    "recommendation": "Use argument lists and keep shell=False.",
                }
            )

    return findings_update(state, "security_scanner", findings)
