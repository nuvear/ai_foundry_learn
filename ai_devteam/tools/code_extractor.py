"""
AI DevTeam — Code Extractor
============================
Parses fenced code blocks with associated filenames from agent markdown output
and writes each block to the correct path under a target directory.

Supports the following filename annotation formats the LLM may produce:

  ### File: backend/app/main.py          (most common)
  ### backend/app/main.py
  **`backend/app/main.py`**
  # File: backend/app/main.py
  `backend/app/main.py`
  backend/app/main.py                    (bare path on its own line)

Followed immediately by a fenced code block:
  ```python
  <code>
  ```
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


# ── Regex patterns ────────────────────────────────────────────────────────────

# Matches a file path — must contain at least one dot (extension) or a slash
_FILE_PATH_RE = re.compile(
    r"(?:"
    r"#{1,4}\s+(?:File:\s*)?[`*]*"    # ### File: or ### or #### etc.
    r"|File:\s*[`*]*"                  # File: prefix
    r"|\*\*[`]"                        # **`
    r"|^[`]"                           # `path`
    r"|^"                              # bare path
    r")"
    r"(?P<path>[a-zA-Z0-9_.][a-zA-Z0-9_./\-]*\.[a-zA-Z0-9]{1,10})"  # the path itself
    r"[`*]*\*?\*?\s*$",               # closing decorators
    re.MULTILINE,
)

# Matches a fenced code block (``` ... ```)
_CODE_BLOCK_RE = re.compile(
    r"```[a-zA-Z0-9_\-]*\n(.*?)```",
    re.DOTALL,
)


def extract_files(markdown: str, target_dir: Path) -> list[Path]:
    """
    Parse `markdown` for (filename, code) pairs and write each to `target_dir`.

    Returns a list of Path objects for every file written.
    Skips blocks where the filename cannot be determined.
    """
    target_dir = Path(target_dir)
    written: list[Path] = []
    seen: set[str] = set()

    # Split on code fences to find annotated blocks
    # Strategy: find each code block, then look backwards for the nearest filename
    lines = markdown.split("\n")
    n = len(lines)

    i = 0
    while i < n:
        line = lines[i]

        # Detect start of a fenced code block
        if line.startswith("```"):
            # Look back up to 5 lines for a filename annotation
            filename = _find_filename_before(lines, i)

            # Collect the code block content
            code_lines = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code = "\n".join(code_lines).strip()

            if filename and code and filename not in seen:
                seen.add(filename)
                out_path = _safe_write(target_dir, filename, code)
                if out_path:
                    written.append(out_path)

        i += 1

    return written


def _find_filename_before(lines: list[str], fence_index: int) -> Optional[str]:
    """
    Look backwards from `fence_index` (exclusive) up to 5 lines to find a
    filename annotation. Returns the normalised path string or None.
    """
    start = max(0, fence_index - 5)
    for j in range(fence_index - 1, start - 1, -1):
        candidate = _extract_path_from_line(lines[j].strip())
        if candidate:
            return candidate
    return None


def _extract_path_from_line(line: str) -> Optional[str]:
    """
    Extract a file path from a single line using the annotation patterns.
    Returns the path string or None.
    """
    if not line:
        return None

    # Normalise common prefixes
    cleaned = line

    # ### File: path  /  # File: path
    cleaned = re.sub(r"^#{1,4}\s+File:\s*", "", cleaned)
    # ### path
    cleaned = re.sub(r"^#{1,4}\s+", "", cleaned)
    # **`path`**  or  **path**
    cleaned = re.sub(r"^\*\*[`]?", "", cleaned)
    cleaned = re.sub(r"[`]?\*\*$", "", cleaned)
    # `path`
    cleaned = re.sub(r"^[`]", "", cleaned)
    cleaned = re.sub(r"[`]$", "", cleaned)
    # File: path
    cleaned = re.sub(r"^File:\s*", "", cleaned)

    cleaned = cleaned.strip().rstrip(":")

    # Must look like a file path (contains a dot for extension, or a slash)
    if not cleaned:
        return None
    if "." not in cleaned and "/" not in cleaned:
        return None
    # Must not contain spaces (would be prose, not a path)
    if " " in cleaned:
        return None
    # Reject lines that are clearly markdown headings or prose
    if cleaned.startswith("#") or cleaned.startswith("*"):
        return None
    # Must have a recognisable extension
    suffix = Path(cleaned).suffix
    if not suffix or len(suffix) > 8:
        return None

    return cleaned


def _safe_write(target_dir: Path, relative_path: str, content: str) -> Optional[Path]:
    """
    Write `content` to `target_dir / relative_path`, creating parent dirs.
    Prevents directory traversal attacks.
    Returns the written Path or None on error.
    """
    try:
        # Resolve relative to target_dir and ensure it stays inside
        out_path = (target_dir / relative_path).resolve()
        if not str(out_path).startswith(str(target_dir.resolve())):
            return None  # Path traversal attempt
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        return out_path
    except Exception:
        return None
