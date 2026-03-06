"""Shared workflow state and helpers for graph nodes."""

from __future__ import annotations

from typing import Any, Literal, TypedDict


Severity = Literal["critical", "high", "medium", "low", "info"]


class Finding(TypedDict, total=False):
    """Normalized finding shape used across all reviewer nodes."""

    id: str
    category: str
    title: str
    description: str
    severity: Severity
    file: str
    line: int
    confidence: float
    source: str
    recommendation: str
    references: list[str]


class CodeReviewState(TypedDict, total=False):
    """Single shared state passed through the whole review graph."""

    code: str
    language: str
    diff: str | None
    metadata: dict[str, Any]
    parsed_diff: list[dict[str, Any]]

    tasks: list[str]
    task_flags: dict[str, bool]

    ast_summary: dict[str, Any]
    call_graph: dict[str, list[str]]
    control_flow: dict[str, int]
    complexity: dict[str, Any]

    findings: list[Finding]
    findings_by_node: dict[str, list[Finding]]
    validated_findings: list[Finding]
    ranked_findings: list[Finding]
    fixes: list[dict[str, Any]]

    report_markdown: str
    overall_score: float
    errors: list[str]


def new_state(
    code: str,
    language: str,
    diff: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> CodeReviewState:
    """Create an initialized state object for graph invocation."""

    return CodeReviewState(
        code=code,
        language=language,
        diff=diff,
        metadata=metadata or {},
        parsed_diff=[],
        tasks=[],
        task_flags={"run_analysis": True, "run_security": True},
        ast_summary={},
        call_graph={},
        control_flow={},
        complexity={},
        findings=[],
        findings_by_node={},
        validated_findings=[],
        ranked_findings=[],
        fixes=[],
        report_markdown="",
        overall_score=100.0,
        errors=[],
    )


def findings_update(state: CodeReviewState, node_name: str, new_findings: list[Finding]) -> dict[str, Any]:
    """Return a partial state update that appends findings for a node."""

    existing_all = list(state.get("findings", []))
    existing_all.extend(new_findings)

    existing_by_node = dict(state.get("findings_by_node", {}))
    existing_node_findings = list(existing_by_node.get(node_name, []))
    existing_node_findings.extend(new_findings)
    existing_by_node[node_name] = existing_node_findings

    return {
        "findings": existing_all,
        "findings_by_node": existing_by_node,
    }


def error_update(state: CodeReviewState, message: str) -> dict[str, Any]:
    """Return an update that appends a processing error into shared state."""

    errors = list(state.get("errors", []))
    errors.append(message)
    return {"errors": errors}
