"""Research agent node: enrich findings with external references."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState, Finding


REFERENCE_MAP = {
    "Dynamic code execution": [
        "https://owasp.org/www-community/attacks/Code_Injection",
        "https://cwe.mitre.org/data/definitions/95.html",
    ],
    "Shell injection risk": [
        "https://owasp.org/www-community/attacks/Command_Injection",
        "https://cwe.mitre.org/data/definitions/78.html",
    ],
}


def research_agent(state: CodeReviewState) -> dict[str, Any]:
    """Attach curated references to selected findings."""

    findings = list(state.get("findings", []))
    updated: list[Finding] = []

    for finding in findings:
        refs = list(finding.get("references", []))
        refs.extend(REFERENCE_MAP.get(finding.get("title", ""), []))
        if refs:
            finding = {**finding, "references": sorted(set(refs))}
        updated.append(finding)

    return {"findings": updated}
