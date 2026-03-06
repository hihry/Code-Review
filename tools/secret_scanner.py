"""Heuristic scanner for hardcoded secrets and credentials."""

from __future__ import annotations

import re
from typing import Any


SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "aws_access_key",
        re.compile(r"AKIA[0-9A-Z]{16}"),
    ),
    (
        "private_key",
        re.compile(r"-----BEGIN (?:RSA |EC |)PRIVATE KEY-----"),
    ),
    (
        "generic_api_key",
        re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*[\"'][^\"']{8,}[\"']"),
    ),
]


def find_potential_secrets(code: str, file: str = "in-memory.py") -> list[dict[str, Any]]:
    """Return potential secrets with line numbers for downstream findings."""

    findings: list[dict[str, Any]] = []
    lines = code.splitlines()

    for idx, line in enumerate(lines, start=1):
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(
                    {
                        "category": "security",
                        "title": f"Potential hardcoded secret ({label})",
                        "description": "A possible secret-like value is present in source code.",
                        "severity": "high",
                        "file": file,
                        "line": idx,
                        "confidence": 0.9,
                        "recommendation": "Move secrets into environment variables or a secret manager.",
                    }
                )
    return findings
