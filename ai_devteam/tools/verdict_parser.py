"""
AI DevTeam — Verdict Parser (Phase 4)
======================================
Parses the structured status line from any agent's output and returns
a normalised verdict: PASS, FAIL, APPROVED, REJECTED, or UNKNOWN.

Every agent's system prompt requires a final status line in one of these forms:
  Status: APPROVED — Ready for Deployment Engineer
  Status: REJECTED — Bugs returned to Developer
  Status: COMPLETE — Ready for [next agent]
  Status: INITIATED — Handing off to Business Analyst

This parser extracts the first keyword after "Status:" and maps it to a
normalised verdict that the Orchestrator PM can act on.
"""

import re
from typing import Literal

Verdict = Literal["PASS", "FAIL", "APPROVED", "REJECTED", "COMPLETE", "UNKNOWN"]

# Map raw status keywords to normalised verdicts
_VERDICT_MAP = {
    "APPROVED":  "APPROVED",
    "REJECTED":  "REJECTED",
    "COMPLETE":  "PASS",
    "INITIATED": "PASS",
    "PASS":      "PASS",
    "FAIL":      "FAIL",
    "FAILED":    "FAIL",
    "BLOCKED":   "FAIL",
}

# The status line pattern used by all agents
_STATUS_PATTERN = re.compile(
    r"^\s*(?:[-#>]\s*)?\*{0,2}Status\*{0,2}[*\s:]*\[?([A-Z]{2,})",
    re.MULTILINE,
)

# Some agents may output a terminal verdict without a "Status:" label
_STANDALONE_VERDICT_PATTERN = re.compile(
    r"^\s*\*{0,2}\[?(APPROVED|REJECTED|PASS|FAIL|FAILED|BLOCKED|COMPLETE|INITIATED)\b",
    re.MULTILINE,
)


def parse_verdict(agent_output: str) -> Verdict:
    """
    Extract the verdict from an agent's output text.

    Returns one of: PASS, FAIL, APPROVED, REJECTED, COMPLETE, UNKNOWN.

    APPROVED and REJECTED are kept distinct from PASS/FAIL because the
    Orchestrator PM treats them differently:
    - APPROVED (from Tester) → advance to Deployment Engineer
    - REJECTED (from Tester) → loop back to Developer
    - PASS (from any other agent) → advance to next agent
    - FAIL → retry or escalate
    - UNKNOWN → treat as FAIL and log a warning
    """
    match = _STATUS_PATTERN.search(agent_output)
    if not match:
        match = _STANDALONE_VERDICT_PATTERN.search(agent_output)
        if not match:
            return "UNKNOWN"

    keyword = match.group(1).upper()
    return _VERDICT_MAP.get(keyword, "UNKNOWN")


def extract_bug_summary(tester_output: str) -> str:
    """
    Extract the bug reports section from a Tester's output.
    Returns the raw text of the Bug Reports section, or an empty string
    if no bugs were found.
    """
    # Look for the Bug Reports section
    bug_section_pattern = re.compile(
        r"###\s*Bug Reports\s*\n(.*?)(?=\n###|\n---|\Z)",
        re.DOTALL | re.IGNORECASE,
    )
    match = bug_section_pattern.search(tester_output)
    if not match:
        return ""
    return match.group(1).strip()


def count_open_bugs(tester_output: str, severity: str = None) -> int:
    """
    Count the number of bug reports in the Tester's output.
    If severity is specified (e.g. 'Critical', 'High'), only count bugs
    of that severity or higher.
    """
    severity_order = ["low", "medium", "high", "critical"]
    min_level = severity_order.index(severity.lower()) if severity else 0

    bug_pattern = re.compile(r"\*\*BUG-\d+:", re.IGNORECASE)
    severity_pattern = re.compile(r"\*\*Severity:\*\*\s*(\w+)", re.IGNORECASE)

    bugs = bug_pattern.findall(tester_output)
    if not severity:
        return len(bugs)

    # Count only bugs at or above the specified severity
    count = 0
    for sev_match in severity_pattern.finditer(tester_output):
        sev = sev_match.group(1).lower()
        if sev in severity_order and severity_order.index(sev) >= min_level:
            count += 1
    return count