"""Cyclomatic and cognitive complexity heuristics."""

from __future__ import annotations

import ast
from typing import Any


class _ComplexityVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.cyclomatic = 1
        self.cognitive = 0
        self.nesting = 0

    def _bump_branch(self) -> None:
        self.cyclomatic += 1
        self.cognitive += 1 + self.nesting

    def generic_visit(self, node: ast.AST) -> Any:
        is_nesting = isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.Match))
        if is_nesting:
            self._bump_branch()
            self.nesting += 1
            super().generic_visit(node)
            self.nesting -= 1
            return
        super().generic_visit(node)


def calculate_complexity(code: str) -> dict[str, int]:
    """Return simple complexity estimates from Python source."""

    tree = ast.parse(code)
    visitor = _ComplexityVisitor()
    visitor.visit(tree)
    return {
        "cyclomatic": visitor.cyclomatic,
        "cognitive": visitor.cognitive,
    }
