"""Entry point for running the LangGraph-powered code review workflow."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from graph.builder import build_graph
from graph.state import CodeReviewState, new_state


def run_review(
    code: str,
    language: str = "auto",
    diff: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> CodeReviewState:
    """Run the full review graph and return final state with report."""

    app = build_graph()
    initial_state = new_state(code=code, language=language, diff=diff, metadata=metadata)
    result = app.invoke(initial_state)
    return CodeReviewState(**result)


def _read_optional_file(path: str | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8")


if __name__ == "__main__":
    # Basic CLI for local usage while keeping run_review as the primary API.
    import argparse

    parser = argparse.ArgumentParser(description="Run static code review over source text.")
    parser.add_argument("code_path", help="Path to source code file")
    parser.add_argument("--language", default="auto", help="Language hint, e.g. python")
    parser.add_argument("--diff-path", default=None, help="Optional unified diff file path")
    args = parser.parse_args()

    code_text = Path(args.code_path).read_text(encoding="utf-8")
    diff_text = _read_optional_file(args.diff_path)
    final_state = run_review(code_text, language=args.language, diff=diff_text)
    print(final_state.get("report_markdown", "No report generated."))
