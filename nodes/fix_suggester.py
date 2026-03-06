"""Fix suggester node: generate patch/refactor guidance snippets."""

from __future__ import annotations

from typing import Any

from graph.state import CodeReviewState


FIX_SNIPPETS = {
    "Mutable default argument": "def f(items: list[str] | None = None) -> None:\n    items = items or []",
    "Bare except clause": "try:\n    ...\nexcept SpecificError as exc:\n    handle(exc)",
    "Dynamic code execution": "SAFE_DISPATCH = {'sum': sum}\nfunc = SAFE_DISPATCH[user_choice]\nresult = func(data)",
    "Shell injection risk": "subprocess.run(['ls', '-la'], check=True, shell=False)",
}


def fix_suggester(state: CodeReviewState) -> dict[str, Any]:
    """Create actionable fix recommendations for top findings."""

    fixes: list[dict[str, Any]] = []

    for finding in state.get("ranked_findings", [])[:10]:
        title = str(finding.get("title", ""))
        snippet = FIX_SNIPPETS.get(title)
        if not snippet:
            continue
        fixes.append(
            {
                "for_title": title,
                "line": finding.get("line", 0),
                "snippet": snippet,
            }
        )

    return {"fixes": fixes}
