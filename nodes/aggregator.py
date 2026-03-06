"""Aggregator node: merge and deduplicate findings across nodes."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState, Finding


def aggregator(state: CodeReviewState) -> dict[str, Any]:
    """Deduplicate findings and produce a unified list."""

    combined = list(state.get("findings", []))
    for node_findings in state.get("findings_by_node", {}).values():
        combined.extend(node_findings)

    seen: set[tuple[str, str, int, str]] = set()
    unique: list[Finding] = []

    for finding in combined:
        key = (
            finding.get("title", ""),
            finding.get("file", ""),
            int(finding.get("line", 0) or 0),
            finding.get("category", ""),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(finding)

    return {"findings": unique}
