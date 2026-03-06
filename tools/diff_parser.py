"""Minimal unified diff parser for patch metadata extraction."""

from __future__ import annotations

import re
from typing import Any


HUNK_RE = re.compile(r"^@@\s+-(\d+)(?:,(\d+))?\s+\+(\d+)(?:,(\d+))?\s+@@")


def parse_unified_diff(diff: str) -> list[dict[str, Any]]:
    """Parse a unified diff into file-level changed-line metadata."""

    if not diff.strip():
        return []

    files: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for line in diff.splitlines():
        if line.startswith("+++ "):
            file_name = line[4:].strip()
            current = {
                "file": file_name,
                "hunks": [],
                "added": 0,
                "removed": 0,
            }
            files.append(current)
            continue

        if current is None:
            continue

        match = HUNK_RE.match(line)
        if match:
            current["hunks"].append(
                {
                    "old_start": int(match.group(1)),
                    "old_count": int(match.group(2) or 1),
                    "new_start": int(match.group(3)),
                    "new_count": int(match.group(4) or 1),
                }
            )
            continue

        if line.startswith("+") and not line.startswith("+++"):
            current["added"] += 1
        elif line.startswith("-") and not line.startswith("---"):
            current["removed"] += 1

    return files
