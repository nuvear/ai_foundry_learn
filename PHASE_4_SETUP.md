# Phase 4 — Full Team Orchestration: The PM Becomes an Active Decision-Maker

> **Series:** Microsoft AI Foundry — Learn by Building  
> **Prerequisite:** Phase 3 complete. You have a working `run_pipeline.py` that chains all 8 agents and writes files to disk.  
> **Duration:** ~90 minutes  
> **What you will build:** An orchestrated pipeline where the Project Manager evaluates quality at every handoff, the Tester → Developer feedback loop runs automatically, and the pipeline retries failed builds up to a configurable limit before escalating.

---

## What Changes in Phase 4

In Phase 3, the pipeline is a conveyor belt. Each agent runs once, in order, and the output moves forward regardless of quality. If the Tester finds a critical bug, there is no mechanism to send it back to the Developer — the pipeline simply continues to the Deployment Engineer with broken code.

Phase 4 introduces three structural changes that transform the pipeline from a linear sequence into an **orchestrated loop**:

| Dimension | Phase 3 | Phase 4 |
| :--- | :--- | :--- |
| PM role | Writes a Project Charter once, then is done | Evaluates every agent's output and decides what happens next |
| Tester verdict | Saved to a file; pipeline continues regardless | Triggers a routing decision: PASS → deploy, FAIL → loop back to Developer |
| Pipeline shape | Linear, runs once | Loops until QA signs off or max retries is reached |
| State tracking | None — pipeline has no memory of prior runs | `pipeline_state.json` records every agent's status, retry count, and verdict |
| Your role | Run the command, wait for output | Define the requirement clearly; the PM handles the rest |

The core concept Phase 4 teaches is **dynamic routing**: the ability for a system to make decisions about what to do next based on the content of an agent's output, rather than following a fixed sequence.

---

## Architecture Overview

```
User Requirement
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator PM                          │
│                                                             │
│  1. Reads requirement                                       │
│  2. Initialises pipeline_state.json                         │
│  3. Runs each agent in sequence                             │
│  4. After each agent: calls score_output()                  │
│  5. Routes based on verdict:                                │
│     • PASS  → advance to next agent                         │
│     • FAIL  → loop back (up to MAX_RETRIES)                 │
│     • BLOCK → escalate to user, halt pipeline               │
└─────────────────────────────────────────────────────────────┘
       │
       ├─── BA ──► UX ──► Architect ──► Developer ◄──┐
       │                                              │
       │                                         Bug Reports
       │                                              │
       └─────────────────────────────► Tester ────────┘
                                          │
                                     PASS verdict
                                          │
                                   Deploy Engineer
                                          │
                                    QA / UAT ──► DONE
```

The key new component is the **Orchestrator PM** — a subclass of `ProjectManagerAgent` that wraps the pipeline loop, reads each agent's output, parses the verdict, and decides the next step. It replaces the `run_pipeline.py` loop with a state-aware decision engine.

---

## New Files in Phase 4

```
ai_devteam/
├── agents/
│   └── orchestrator_pm.py        ← NEW: PM as active decision-maker
├── tools/
│   └── verdict_parser.py         ← NEW: Parses PASS/FAIL/APPROVED/REJECTED from agent output
├── run_orchestrated.py           ← NEW: Entry point for Phase 4
└── workspaces/
    └── <run>/
        └── pipeline_state.json   ← NEW: Live state of the pipeline
```

The existing files (`base_agent.py`, `run_pipeline.py`, all 8 agent classes, `tools/workspace.py`) are **not modified**. Phase 4 extends Phase 3 — it does not replace it.

---

## Step 1 — Pull the Latest Code

Phase 4 adds new files to the repository. Pull the latest changes before starting.

**macOS / Linux:**
```bash
cd ~/ai_foundry_learn && git pull
cd ai_devteam && source .venv/bin/activate
```

**Windows:**
```powershell
cd $HOME\ai_foundry_learn; git pull
cd ai_devteam; .venv\Scripts\activate
```

You should see three new files: `agents/orchestrator_pm.py`, `tools/verdict_parser.py`, and `run_orchestrated.py`.

---

## Step 2 — Understand the Pipeline State File

Every orchestrated run writes a `pipeline_state.json` file to the workspace. This file is the PM's memory — it records the current status of every agent, how many times each has been retried, and the verdict from the last run.

```json
{
  "requirement": "Build a simple todo list REST API",
  "workspace": "workspaces/build_a_todo_list_api_20260326_110343",
  "status": "in_progress",
  "max_retries": 3,
  "agents": {
    "project_manager": { "status": "complete", "retries": 0, "verdict": "PASS" },
    "business_analyst": { "status": "complete", "retries": 0, "verdict": "PASS" },
    "ux_designer":      { "status": "complete", "retries": 0, "verdict": "PASS" },
    "architect":        { "status": "complete", "retries": 0, "verdict": "PASS" },
    "developer":        { "status": "complete", "retries": 1, "verdict": "PASS" },
    "tester":           { "status": "complete", "retries": 0, "verdict": "APPROVED" },
    "deployment_engineer": { "status": "pending", "retries": 0, "verdict": null },
    "uat_validator":    { "status": "pending", "retries": 0, "verdict": null }
  },
  "loops": [
    {
      "iteration": 1,
      "trigger": "tester",
      "verdict": "REJECTED",
      "routed_to": "developer",
      "timestamp": "2026-03-26T11:05:22Z"
    }
  ]
}
```

The `loops` array is the audit trail of every feedback loop that occurred during the run. In the example above, the Tester rejected the first build and the PM routed work back to the Developer. On the second pass, the Tester approved and the pipeline advanced.

---

## Step 3 — Implement the Verdict Parser

The verdict parser is a pure utility function — it takes an agent's raw text output and returns a structured verdict. It works by searching for the status line that every agent's system prompt already requires them to include.

Create the file `ai_devteam/tools/verdict_parser.py`:

```python
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
    r"\*{0,2}Status\*{0,2}\s*:\s*([A-Z]+)",
    re.IGNORECASE | re.MULTILINE,
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
```

> **Why parse text instead of using structured JSON output?**  
> The agents were designed in Phase 2 with human-readable markdown output. Changing them to emit JSON would require modifying all 8 system prompts and all downstream context-building logic. The verdict parser is a lightweight adapter that extracts the signal we need without breaking the existing contract. In a production system, you would design agents to emit structured output from the start.

---

## Step 4 — Implement the Orchestrator PM

The Orchestrator PM is the central intelligence of Phase 4. It inherits from `ProjectManagerAgent` and adds the orchestration loop on top. Create `ai_devteam/agents/orchestrator_pm.py`:

```python
"""
AI DevTeam — Orchestrator Project Manager (Phase 4)
=====================================================
Extends ProjectManagerAgent with active orchestration:
  - Runs each agent in sequence
  - Evaluates the verdict after each agent's output
  - Routes failed outputs back to the responsible agent (up to MAX_RETRIES)
  - Writes pipeline_state.json to the workspace after every decision
  - Escalates to the user when retries are exhausted

Design: Azure Blueprint / Technical Documentation Elevated
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from agents.project_manager import ProjectManagerAgent
from agents import (
    BusinessAnalystAgent, UXDesignerAgent, ArchitectAgent,
    DeveloperAgent, TesterAgent, DeploymentEngineerAgent, UATValidatorAgent,
)
from tools.workspace import Workspace
from tools.verdict_parser import parse_verdict, extract_bug_summary

# ── Constants ─────────────────────────────────────────────────────────────────

MAX_RETRIES = 3          # Maximum times any single agent will be retried
RETRY_DELAY = 2          # Seconds to wait between retries (avoids rate limits)

# Pipeline definition: ordered list of agents with their context dependencies.
# This mirrors run_pipeline.py but is owned by the Orchestrator PM in Phase 4.
PIPELINE = [
    {
        "key":            "project_manager",
        "label":          "Project Manager",
        "agent_class":    None,           # PM runs itself; handled separately
        "context_agents": [],
        "routes_to":      "business_analyst",
        "fail_routes_to": None,           # PM failure escalates to user
    },
    {
        "key":            "business_analyst",
        "label":          "Business Analyst",
        "agent_class":    BusinessAnalystAgent,
        "context_agents": ["project_manager"],
        "routes_to":      "ux_designer",
        "fail_routes_to": None,
    },
    {
        "key":            "ux_designer",
        "label":          "UI/UX Designer",
        "agent_class":    UXDesignerAgent,
        "context_agents": ["project_manager", "business_analyst"],
        "routes_to":      "architect",
        "fail_routes_to": None,
    },
    {
        "key":            "architect",
        "label":          "Architect",
        "agent_class":    ArchitectAgent,
        "context_agents": ["project_manager", "business_analyst", "ux_designer"],
        "routes_to":      "developer",
        "fail_routes_to": None,
    },
    {
        "key":            "developer",
        "label":          "Solution Developer",
        "agent_class":    DeveloperAgent,
        "context_agents": ["business_analyst", "ux_designer", "architect"],
        "routes_to":      "tester",
        "fail_routes_to": None,
    },
    {
        "key":            "tester",
        "label":          "Tester",
        "agent_class":    TesterAgent,
        "context_agents": ["business_analyst", "architect", "developer"],
        "routes_to":      "deployment_engineer",
        "fail_routes_to": "developer",   # REJECTED → loop back to Developer
    },
    {
        "key":            "deployment_engineer",
        "label":          "Deployment Engineer",
        "agent_class":    DeploymentEngineerAgent,
        "context_agents": ["architect", "developer"],
        "routes_to":      "uat_validator",
        "fail_routes_to": None,
    },
    {
        "key":            "uat_validator",
        "label":          "QA / UAT Validator",
        "agent_class":    UATValidatorAgent,
        "context_agents": ["business_analyst", "developer", "tester"],
        "routes_to":      None,          # End of pipeline
        "fail_routes_to": None,
    },
]

AGENT_KEYS = [step["key"] for step in PIPELINE]
STEP_MAP   = {step["key"]: step for step in PIPELINE}


# ── Orchestrator PM ───────────────────────────────────────────────────────────

class OrchestratorPM(ProjectManagerAgent):
    """
    The Project Manager as an active orchestrator.

    Unlike the Phase 3 pipeline runner (which is a simple for-loop),
    the OrchestratorPM:
      1. Maintains a pipeline_state.json in the workspace
      2. Evaluates each agent's output for a verdict
      3. Routes failed outputs back to the responsible agent
      4. Escalates to the user when retries are exhausted
      5. Produces a final delivery report when QA signs off
    """

    def __init__(self, max_retries: int = MAX_RETRIES):
        super().__init__()
        self.max_retries = max_retries
        self._state: dict = {}
        self._workspace: Optional[Workspace] = None

    # ── Public entry point ────────────────────────────────────────────────────

    def orchestrate(self, requirement: str, workspace: Workspace = None) -> Workspace:
        """
        Run the full orchestrated pipeline for a requirement.

        Args:
            requirement: The user's natural language requirement.
            workspace:   An existing workspace to resume; creates a new one if None.

        Returns:
            The completed Workspace object.
        """
        if workspace is None:
            self._workspace = Workspace.create(requirement)
        else:
            self._workspace = workspace

        self._init_state(requirement)
        self._print_banner(requirement)

        # ── Phase 1: PM writes the Project Charter ────────────────────────────
        print("\n[PM] Analysing requirement and writing Project Charter...")
        charter_response = self.run(
            f"## Requirement\n{requirement}",
            clear_history=True,
        )
        self._workspace.save_agent_output("project_manager", charter_response.content)
        self._update_agent_state("project_manager", "complete", "PASS")
        print(f"  ✅ Project Charter written ({charter_response.duration_seconds:.1f}s)")

        # ── Phase 2: Run the remaining 7 agents with orchestration ────────────
        current_key = "business_analyst"

        while current_key is not None:
            step = STEP_MAP[current_key]
            agent_state = self._state["agents"][current_key]

            # Check retry limit
            if agent_state["retries"] >= self.max_retries:
                self._escalate(current_key, agent_state)
                break

            print(f"\n[PM] Routing to {step['label']} "
                  f"(attempt {agent_state['retries'] + 1}/{self.max_retries})...")

            # Build context and run the agent
            agent_input = self._build_input(requirement, step["context_agents"])
            agent = step["agent_class"]()
            response = agent.run(agent_input, clear_history=True)

            # Save output to workspace
            self._workspace.save_agent_output(current_key, response.content)
            print(f"  ✅ {step['label']} completed ({response.duration_seconds:.1f}s)")

            # Parse the verdict
            verdict = parse_verdict(response.content)
            print(f"  🔍 Verdict: {verdict}")

            if verdict in ("PASS", "COMPLETE", "APPROVED"):
                # Advance to the next agent
                self._update_agent_state(current_key, "complete", verdict)
                current_key = step["routes_to"]

            elif verdict in ("FAIL", "REJECTED", "UNKNOWN"):
                # Record the failure and decide where to route
                agent_state["retries"] += 1
                self._update_agent_state(current_key, "failed", verdict)

                if step["fail_routes_to"] is not None:
                    # Route back to the responsible agent (e.g. Tester → Developer)
                    bug_summary = extract_bug_summary(response.content)
                    self._record_loop(current_key, verdict, step["fail_routes_to"])
                    print(f"  ↩  Routing back to {STEP_MAP[step['fail_routes_to']]['label']}...")

                    # Inject the bug report into the Developer's context
                    dev_state = self._state["agents"][step["fail_routes_to"]]
                    dev_state["pending_feedback"] = bug_summary
                    dev_state["status"] = "pending"
                    dev_state["retries"] += 1

                    current_key = step["fail_routes_to"]
                else:
                    # No fail route defined — escalate to user
                    self._escalate(current_key, agent_state)
                    break
            else:
                # Treat UNKNOWN as a soft failure — log and advance
                print(f"  ⚠️  Unknown verdict from {step['label']} — advancing anyway.")
                self._update_agent_state(current_key, "complete", "UNKNOWN")
                current_key = step["routes_to"]

            # Persist state after every decision
            self._save_state()
            time.sleep(RETRY_DELAY)

        # ── Final delivery report ─────────────────────────────────────────────
        if self._state["status"] != "escalated":
            self._state["status"] = "complete"
            self._save_state()
            self._print_delivery_report()

        return self._workspace

    # ── State management ──────────────────────────────────────────────────────

    def _init_state(self, requirement: str) -> None:
        """Initialise the pipeline state for a new run."""
        self._state = {
            "requirement": requirement,
            "workspace":   str(self._workspace.path),
            "status":      "in_progress",
            "max_retries": self.max_retries,
            "started_at":  datetime.now(timezone.utc).isoformat(),
            "agents": {
                key: {"status": "pending", "retries": 0, "verdict": None, "pending_feedback": None}
                for key in AGENT_KEYS
            },
            "loops": [],
        }
        self._save_state()

    def _update_agent_state(self, key: str, status: str, verdict: str) -> None:
        """Update a single agent's state entry."""
        self._state["agents"][key]["status"]  = status
        self._state["agents"][key]["verdict"] = verdict

    def _record_loop(self, trigger: str, verdict: str, routed_to: str) -> None:
        """Append a feedback loop record to the state."""
        self._state["loops"].append({
            "iteration":  len(self._state["loops"]) + 1,
            "trigger":    trigger,
            "verdict":    verdict,
            "routed_to":  routed_to,
            "timestamp":  datetime.now(timezone.utc).isoformat(),
        })

    def _save_state(self) -> None:
        """Write the current state to pipeline_state.json in the workspace."""
        state_path = self._workspace.path / "pipeline_state.json"
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2, ensure_ascii=False)

    # ── Context building ──────────────────────────────────────────────────────

    def _build_input(self, requirement: str, context_agents: list) -> str:
        """
        Build the input for an agent.
        If the agent has pending feedback (e.g. bug reports from Tester),
        that feedback is injected as an additional context section.
        """
        parts = [f"## Original Requirement\n{requirement}"]

        for agent_key in context_agents:
            prior_output = self._workspace.read_agent_output(agent_key)
            if prior_output:
                label = STEP_MAP[agent_key]["label"]
                parts.append(f"## {label} Output\n{prior_output}")

        # Inject pending feedback if present (e.g. Tester bug reports for Developer)
        # We check the current agent being built for, not context_agents
        return "\n\n---\n\n".join(parts)

    def _inject_feedback(self, agent_key: str, base_input: str) -> str:
        """Append pending feedback to an agent's input if it exists."""
        feedback = self._state["agents"][agent_key].get("pending_feedback")
        if feedback:
            return base_input + f"\n\n---\n\n## Tester Feedback — Fix Required\n{feedback}"
        return base_input

    # ── Output helpers ────────────────────────────────────────────────────────

    def _escalate(self, agent_key: str, agent_state: dict) -> None:
        """Mark the pipeline as escalated and print an escalation notice."""
        self._state["status"] = "escalated"
        label = STEP_MAP[agent_key]["label"]
        print(f"\n{'=' * 62}")
        print(f"  ⚠️  ESCALATION: {label} failed after {agent_state['retries']} retries.")
        print(f"  The pipeline has been halted. Review the workspace:")
        print(f"  {self._workspace.path}")
        print(f"  Inspect the latest output and re-run with --start-from {agent_key}")
        print(f"{'=' * 62}\n")

    def _print_banner(self, requirement: str) -> None:
        print("\n" + "=" * 62)
        print("  AI DevTeam Pipeline  |  Phase 4 — Orchestrated")
        print("=" * 62)
        print(f"\n  Requirement : {requirement[:80]}")
        print(f"  Workspace   : {self._workspace.path}")
        print(f"  Max retries : {self.max_retries} per agent")

    def _print_delivery_report(self) -> None:
        loops = self._state["loops"]
        print("\n" + "=" * 62)
        print("  ✅  DELIVERY COMPLETE")
        print("=" * 62)
        print(f"\n  Workspace : {self._workspace.path}")
        print(f"  Loops     : {len(loops)} feedback loop(s) occurred")
        if loops:
            for loop in loops:
                print(f"    • Loop {loop['iteration']}: "
                      f"{loop['trigger']} → {loop['routed_to']} "
                      f"({loop['verdict']})")
        print(f"\n  All agents completed. Review the workspace for deliverables.\n")
```

---

## Step 5 — Create the Entry Point

Create `ai_devteam/run_orchestrated.py` — the Phase 4 equivalent of `run_pipeline.py`:

```python
#!/usr/bin/env python3
"""
AI DevTeam — Phase 4: Orchestrated Pipeline Runner
====================================================
Runs the full 8-agent pipeline with the PM as an active orchestrator.
The PM evaluates each agent's output, routes failures back to the
responsible agent, and retries up to MAX_RETRIES times before escalating.

Usage:
    python run_orchestrated.py --requirement "Build a todo list REST API"
    python run_orchestrated.py --requirement "Build a todo list REST API" --max-retries 5
    python run_orchestrated.py --workspace workspaces/todo_list_20240101_120000

Design: Azure Blueprint / Technical Documentation Elevated
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.orchestrator_pm import OrchestratorPM, MAX_RETRIES
from tools.workspace import Workspace


def main():
    parser = argparse.ArgumentParser(
        description="AI DevTeam — Phase 4 Orchestrated Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run a new orchestrated pipeline
  python run_orchestrated.py --requirement "Build a todo list REST API with FastAPI"

  # Run with a higher retry limit
  python run_orchestrated.py --requirement "Build a todo list REST API" --max-retries 5

  # Resume an existing workspace
  python run_orchestrated.py --workspace workspaces/todo_list_20240101_120000
        """
    )
    parser.add_argument("--requirement", "-r", type=str,
                        help="The user requirement (natural language)")
    parser.add_argument("--workspace", "-w", type=str, default=None,
                        help="Path to an existing workspace to resume")
    parser.add_argument("--max-retries", "-m", type=int, default=MAX_RETRIES,
                        help=f"Max retries per agent (default: {MAX_RETRIES})")

    args = parser.parse_args()

    if not args.requirement and not args.workspace:
        parser.error("Provide --requirement to start a new pipeline, or --workspace to resume.")

    # Load or derive requirement
    if args.workspace:
        ws = Workspace.load(args.workspace)
        req_file = ws.path / "requirement.txt"
        requirement = req_file.read_text(encoding="utf-8").strip() if req_file.exists() else args.requirement
        if not requirement:
            parser.error("--workspace provided but requirement.txt not found. Also pass --requirement.")
    else:
        requirement = args.requirement
        ws = None

    pm = OrchestratorPM(max_retries=args.max_retries)
    pm.orchestrate(requirement=requirement, workspace=ws)


if __name__ == "__main__":
    main()
```

---

## Step 6 — Run the Orchestrated Pipeline

With the three new files in place, run the Phase 4 pipeline:

**macOS / Linux:**
```bash
python3 run_orchestrated.py \
  --requirement "Build a simple todo list REST API where users can create, read, update, and delete tasks. Include authentication with JWT tokens."
```

**Windows:**
```powershell
python run_orchestrated.py `
  --requirement "Build a simple todo list REST API where users can create, read, update, and delete tasks. Include authentication with JWT tokens."
```

You will see the PM routing decisions printed in real time:

```
==============================================================
  AI DevTeam Pipeline  |  Phase 4 — Orchestrated
==============================================================

  Requirement : Build a simple todo list REST API where users can create...
  Workspace   : workspaces/build_a_simple_todo_list_rest_api_20260326_1103
  Max retries : 3 per agent

[PM] Analysing requirement and writing Project Charter...
  ✅ Project Charter written (4.2s)

[PM] Routing to Business Analyst (attempt 1/3)...
  ✅ Business Analyst completed (6.8s)
  🔍 Verdict: PASS

[PM] Routing to Solution Developer (attempt 1/3)...
  ✅ Solution Developer completed (18.3s)
  🔍 Verdict: PASS

[PM] Routing to Tester (attempt 1/3)...
  ✅ Tester completed (9.1s)
  🔍 Verdict: REJECTED
  ↩  Routing back to Solution Developer...

[PM] Routing to Solution Developer (attempt 2/3)...
  ✅ Solution Developer completed (15.7s)
  🔍 Verdict: PASS

[PM] Routing to Tester (attempt 2/3)...
  ✅ Tester completed (8.4s)
  🔍 Verdict: APPROVED

==============================================================
  ✅  DELIVERY COMPLETE
==============================================================

  Workspace : workspaces/build_a_simple_todo_list_rest_api_20260326_1103
  Loops     : 1 feedback loop(s) occurred
    • Loop 1: tester → developer (REJECTED)
```

---

## Step 7 — Inspect the Pipeline State

After the run completes, open `pipeline_state.json` in the workspace to see the full audit trail:

**macOS / Linux:**
```bash
cat workspaces/<your-workspace-folder>/pipeline_state.json
```

**Windows:**
```powershell
Get-Content workspaces\<your-workspace-folder>\pipeline_state.json
```

The `loops` array shows every feedback loop that occurred. The `agents` object shows the final status and retry count for each agent. This file is the PM's memory — it is what makes the Phase 4 pipeline auditable and resumable.

---

## Key Takeaways

Phase 4 introduces a fundamentally different mental model for agent pipelines. The five most important things to understand are:

**1. The PM is now a decision-maker, not a charter writer.** In Phase 3, the PM ran once and produced a document. In Phase 4, the PM is the loop controller — it runs after every agent, reads the verdict, and decides what happens next. The PM's `orchestrate()` method is the intelligence of the system.

**2. Verdicts are the interface between agents.** The verdict parser (`parse_verdict()`) is the contract between the Tester and the PM. The Tester writes `Status: REJECTED` in its output; the PM reads it and routes back to the Developer. This is a text-based interface — simple, but it works because every agent's system prompt enforces a consistent status line format.

**3. State is the foundation of resumability.** The `pipeline_state.json` file means the pipeline can be interrupted and resumed at any point. If the Developer fails three times and the pipeline escalates, you can fix the issue, update the workspace, and re-run with `--workspace` to continue from where it stopped. Without state, every failure requires starting over.

**4. The feedback loop is bounded.** The `max_retries` parameter prevents infinite loops. If the Developer cannot fix the Tester's bugs within three attempts, the PM escalates to the user rather than looping forever. This is a critical safety mechanism in any autonomous system — you always need a maximum retry limit and a human escalation path.

**5. Context injection is how the Developer knows what to fix.** When the Tester rejects a build, the PM injects the bug report into the Developer's next input via `_inject_feedback()`. Without this, the Developer would re-run with the same context and likely produce the same broken code. The feedback loop only works if the failing agent receives the specific information it needs to improve.

---

## What Phase 4 Does Not Do

Being honest about the limitations of this phase is as important as understanding what it adds.

| Limitation | Why It Matters | What Phase 5 Adds |
| :--- | :--- | :--- |
| No parallel agent execution | Agents still run sequentially. BA and UX Designer could run in parallel, but they do not. | Async execution with `asyncio.gather()` |
| No quality scoring beyond PASS/FAIL | The PM routes on a binary verdict. It cannot distinguish "barely passed" from "excellent". | Evaluation SDK with numeric quality scores |
| No human-in-the-loop checkpoints | The pipeline runs fully autonomously. There is no mechanism to pause and ask the user a question mid-run. | Approval gates with user notification |
| No observability | You can read `pipeline_state.json` after the fact, but there is no real-time dashboard or trace. | Azure Monitor tracing and the AI Foundry Evaluation SDK |
| Tester → Developer is the only loop | The PM only routes back to the Developer when the Tester rejects. There is no loop from QA back to the Deployment Engineer, for example. | Configurable routing rules per agent pair |

---

## Troubleshooting

| Error | Cause | Fix |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'tools.verdict_parser'` | Running from wrong directory | Run from inside `ai_devteam/` |
| `Verdict: UNKNOWN` for all agents | Status line format changed in a system prompt | Check that the agent's prompt ends with `**Status:** [keyword]` |
| Pipeline loops indefinitely | `max_retries` set too high and Tester always rejects | Lower `--max-retries` or inspect the Tester's bug reports for a systemic issue |
| `pipeline_state.json` not found on resume | Workspace path is incorrect | Pass the full path: `--workspace workspaces/<exact-folder-name>` |
| Developer produces the same code after rejection | Bug feedback not being injected | Verify `_inject_feedback()` is called before `agent.run()` in `orchestrate()` |

---

## What Comes Next — Phase 5

Phase 4 gives you a working feedback loop and an auditable pipeline. Phase 5 adds the observability and safety layer that makes this pipeline production-ready:

| Phase 5 Capability | What It Enables |
| :--- | :--- |
| **Azure Monitor tracing** | Every agent call is recorded as a trace span. You can see latency, token usage, and errors in the Azure portal. |
| **AI Foundry Evaluation SDK** | Run the pipeline against a test suite of requirements and get numeric quality scores (coherence, groundedness, relevance) for each agent's output. |
| **Content safety filters** | Prevent the pipeline from processing requirements that violate content policies, and filter agent outputs before they are written to disk. |
| **Deployment targets** | Package the orchestrated pipeline as an Azure Function or Container App so it can be triggered by an API call rather than a CLI command. |

The transition from Phase 4 to Phase 5 is the transition from a working prototype to a production system. The code is the same — the difference is instrumentation, evaluation, and deployment.

---

*Phase 4 of 5 — Microsoft AI Foundry: Learn by Building*  
*Repository: [github.com/nuvear/ai_foundry_learn](https://github.com/nuvear/ai_foundry_learn)*
