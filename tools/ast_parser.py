"""AST parser utility for Python source analysis."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PythonAstSummary:
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)


class _AstAnalyzer(ast.NodeVisitor):
    def __init__(self) -> None:
        self.summary = PythonAstSummary()
        self.call_graph: dict[str, list[str]] = {}
        self.control_flow = {"if": 0, "for": 0, "while": 0, "try": 0}
        self._current_function: str | None = None

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.summary.classes.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.summary.functions.append(node.name)
        prev = self._current_function
        self._current_function = node.name
        self.call_graph.setdefault(node.name, [])
        self.generic_visit(node)
        self._current_function = prev

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.visit_FunctionDef(node)  # Reuse same handling.

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            self.summary.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        module = node.module or ""
        self.summary.imports.append(module)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> Any:
        self.control_flow["if"] += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> Any:
        self.control_flow["for"] += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> Any:
        self.control_flow["while"] += 1
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> Any:
        self.control_flow["try"] += 1
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        if self._current_function is not None:
            called_name = _name_from_call(node)
            if called_name:
                self.call_graph.setdefault(self._current_function, []).append(called_name)
        self.generic_visit(node)


def _name_from_call(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def parse_python_code(source: str) -> dict[str, Any]:
    """Parse Python source and return structured AST metadata."""

    tree = ast.parse(source)
    analyzer = _AstAnalyzer()
    analyzer.visit(tree)

    return {
        "summary": {
            "functions": analyzer.summary.functions,
            "classes": analyzer.summary.classes,
            "imports": analyzer.summary.imports,
        },
        "call_graph": analyzer.call_graph,
        "control_flow": analyzer.control_flow,
    }
