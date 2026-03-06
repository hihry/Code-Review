"""Shared pytest fixtures for code review tests."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest


FIXTURE_DIR = Path(__file__).parent / "fixtures"
ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture
def sample_code() -> str:
    return (FIXTURE_DIR / "sample.py").read_text(encoding="utf-8")


@pytest.fixture
def sample_patch() -> str:
    return (FIXTURE_DIR / "sample.patch").read_text(encoding="utf-8")
