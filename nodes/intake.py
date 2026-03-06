"""Intake node: language detection, diff parsing, and metadata enrichment."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState
from tools.diff_parser import parse_unified_diff


def _detect_language(code: str, declared: str) -> str:
    if declared and declared.lower() != "auto":
        return declared.lower()
    if "def " in code or "import " in code:
        return "python"
    if "function " in code or "const " in code:
        return "javascript"
    return "unknown"


def intake(state: CodeReviewState) -> dict[str, Any]:
    """Prepare baseline metadata for downstream planning and analyzers."""

    code = state.get("code", "")
    language = _detect_language(code, state.get("language", "auto"))
    diff = state.get("diff") or ""
    parsed_diff = parse_unified_diff(diff)

    metadata = dict(state.get("metadata", {}))
    metadata.update(
        {
            "line_count": len(code.splitlines()),
            "char_count": len(code),
            "diff_files": len(parsed_diff),
            "has_diff": bool(parsed_diff),
        }
    )

    return {
        "language": language,
        "parsed_diff": parsed_diff,
        "metadata": metadata,
    }
