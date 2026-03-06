# Code Review Graph

LangGraph-based code review pipeline with modular analyzers, security scanning, ranking, and markdown report generation.

## Structure

- `graph/`: shared state, routing logic, and graph builder
- `nodes/`: individual analyzers and report nodes
- `chains/`: stage-level orchestration pipelines
- `tools/`: reusable parsers and heuristics
- `tests/`: unit tests and sample fixtures
- `main.py`: `run_review(code, language)` entry point

## Quick Start

```bash
poetry install
poetry run python main.py tests/fixtures/sample.py --language python --diff-path tests/fixtures/sample.patch
```

## Programmatic Usage

```python
from main import run_review

source = "def add(a, b):\n    return a + b\n"
result = run_review(source, language="python")
print(result["report_markdown"])
```

## Test

```bash
poetry run pytest -q
```
