"""Report generator node: markdown output and final score summary."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState


def report_generator(state: CodeReviewState) -> dict[str, Any]:
    """Build a final markdown report from ranked findings and fixes."""

    findings = state.get("ranked_findings", [])
    score = state.get("overall_score", 100.0)
    tasks = state.get("tasks", [])

    lines = [
        "# Code Review Report",
        "",
        f"Overall Score: **{score}/100**",
        "",
        "## Pipeline",
    ]

    for task in tasks:
        lines.append(f"- {task}")

    lines.extend(["", "## Findings"])

    if not findings:
        lines.append("- No findings detected.")
    else:
        for idx, finding in enumerate(findings, start=1):
            title = finding.get("title", "Untitled")
            severity = str(finding.get("severity", "info")).upper()
            line = finding.get("line", "?")
            desc = finding.get("description", "")
            lines.append(f"{idx}. [{severity}] {title} (line {line})")
            lines.append(f"   - {desc}")

    fixes = state.get("fixes", [])
    lines.extend(["", "## Suggested Fixes"])
    if not fixes:
        lines.append("- No automatic fix snippets available.")
    else:
        for fix in fixes:
            lines.append(f"- {fix['for_title']} (line {fix['line']})")
            lines.append("```python")
            lines.append(str(fix["snippet"]))
            lines.append("```")

    return {"report_markdown": "\n".join(lines)}
