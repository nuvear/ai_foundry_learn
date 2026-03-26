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
import re
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
            agent_input = self._build_input(requirement, step["context_agents"], current_key)
            agent = step["agent_class"]()
            response = agent.run(agent_input, clear_history=True)

            # Save output to workspace
            self._workspace.save_agent_output(current_key, response.content)
            print(f"  ✅ {step['label']} completed ({response.duration_seconds:.1f}s)")

            # Parse the verdict
            verdict = parse_verdict(response.content)

            # Hardening gate: if Developer has pending tester feedback, it must
            # explicitly acknowledge all BUG IDs before a pass can be accepted.
            if current_key == "developer" and verdict in ("PASS", "COMPLETE", "APPROVED", "UNKNOWN"):
                pending_feedback = agent_state.get("pending_feedback")
                if pending_feedback and not self._developer_acknowledged_feedback(response.content, pending_feedback):
                    print("  ⚠️  Developer output did not acknowledge all pending BUG IDs — forcing retry.")
                    verdict = "FAIL"

            print(f"  🔍 Verdict: {verdict}")

            if verdict in ("PASS", "COMPLETE", "APPROVED", "UNKNOWN"):
                # Advance to the next agent
                # UNKNOWN = could not parse status line, treat as pass and advance
                if verdict == "UNKNOWN":
                    print(f"  ⚠️  Could not parse verdict from {step['label']} — advancing.")
                self._update_agent_state(current_key, "complete", verdict)

                # Developer resolved feedback successfully; clear pending bugs.
                if current_key == "developer":
                    agent_state["pending_feedback"] = None

                current_key = step["routes_to"]

            elif verdict in ("FAIL", "REJECTED"):
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

                    current_key = step["fail_routes_to"]
                else:
                    if agent_state["retries"] < self.max_retries:
                        agent_state["retries"] += 1  # increment before printing so the count is accurate
                        print(f"  ↩  Retrying {step['label']} (attempt {agent_state['retries']}/{self.max_retries})...")
                        # current_key stays the same — loop will re-run this agent
                    else:
                        self._escalate(current_key, agent_state)
                    break

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

    def _build_input(self, requirement: str, context_agents: list, agent_key: str) -> str:
        """
        Build the input for an agent.
        If the agent has pending feedback (e.g. bug reports from Tester),
        that feedback is injected as an additional context section.
        """
        parts = [f"## Original Requirement\n{requirement}"]

        for agent_key_ctx in context_agents:
            prior_output = self._workspace.read_agent_output(agent_key_ctx)
            if prior_output:
                label = STEP_MAP[agent_key_ctx]["label"]
                parts.append(f"## {label} Output\n{prior_output}")

        base_input = "\n\n---\n\n".join(parts)
        return self._inject_feedback(agent_key, base_input)

    def _inject_feedback(self, agent_key: str, base_input: str) -> str:
        """Append pending feedback to an agent's input if it exists."""
        feedback = self._state["agents"][agent_key].get("pending_feedback")
        if feedback:
            return base_input + f"\n\n---\n\n## Tester Feedback — Fix Required\n{feedback}"
        return base_input

    def _developer_acknowledged_feedback(self, developer_output: str, pending_feedback: str) -> bool:
        """
        Ensure Developer acknowledges every pending BUG ID before pass-through.
        """
        required_bug_ids = set(re.findall(r"BUG-\d+", pending_feedback, flags=re.IGNORECASE))
        if not required_bug_ids:
            return True

        output_bug_ids = set(re.findall(r"BUG-\d+", developer_output, flags=re.IGNORECASE))
        if not required_bug_ids.issubset(output_bug_ids):
            return False

        return "bug fix summary" in developer_output.lower()

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