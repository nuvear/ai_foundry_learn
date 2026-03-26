#!/usr/bin/env python3
# =============================================================================
# AI DevTeam — Single Agent Runner (Phase 2)
# =============================================================================
# Usage:
#   python run_agent.py --agent <name> --input "<your message>"
#   python run_agent.py --agent pm --input "Build a weather dashboard app"
#   python run_agent.py --agent developer --input "Write a REST API for a todo list"
#   python run_agent.py --list
#
# Available agent names:
#   pm, ba, ux, architect, developer, tester, deploy, qa
# =============================================================================

import argparse
import sys
import os
import time
from pathlib import Path

# Add the ai_devteam directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from shared.config import config


def print_banner():
    print("\n" + "=" * 65)
    print("  AI DevTeam — Single Agent Runner  |  Phase 2")
    print("=" * 65)


def print_agent_list():
    """Print all available agents and their descriptions."""
    agents_info = [
        ("pm",         "Project Manager",      "Creates Project Charter, orchestrates the pipeline"),
        ("ba",         "Business Analyst",     "Produces FRD, User Stories, Acceptance Criteria"),
        ("ux",         "UI/UX Designer",       "Wireframes, User Flows, Component Specifications"),
        ("architect",  "Architect",            "HLD, Tech Stack, API Contracts, Data Models"),
        ("developer",  "Solution Developer",   "Source Code, Unit Tests, README"),
        ("tester",     "Tester",               "Test Plan, Test Cases, Bug Reports"),
        ("deploy",     "Deployment Engineer",  "Dockerfile, CI/CD Pipeline, Deployment Guide"),
        ("qa",         "QA / UAT Validator",   "UAT Scenarios, Final Sign-off"),
    ]
    print("\nAvailable Agents:")
    print("-" * 65)
    print(f"  {'Key':<12} {'Agent Name':<22} {'Produces'}")
    print("-" * 65)
    for key, name, desc in agents_info:
        print(f"  {key:<12} {name:<22} {desc}")
    print("-" * 65)
    print("\nExample:")
    print('  python run_agent.py --agent pm --input "Build a todo list app"\n')


def run_agent(agent_key: str, user_input: str) -> None:
    """Instantiate the requested agent and run it with the given input."""

    # Import here to avoid loading all agents unless needed
    from agents import AGENT_REGISTRY

    agent_key = agent_key.lower().strip()

    if agent_key not in AGENT_REGISTRY:
        print(f"\n  ERROR: Unknown agent '{agent_key}'")
        print(f"  Run 'python run_agent.py --list' to see available agents.\n")
        sys.exit(1)

    # Instantiate the agent
    AgentClass = AGENT_REGISTRY[agent_key]
    agent = AgentClass()

    print(f"\n  Agent  : {agent.name}")
    print(f"  Model  : {agent.model_deployment}")
    print(f"  Input  : {user_input[:80]}{'...' if len(user_input) > 80 else ''}")
    print("\n" + "-" * 65)
    print("  Thinking...\n")

    start = time.time()

    try:
        response = agent.run(user_input)
    except Exception as e:
        print(f"\n  ERROR: Agent failed with: {e}")
        print("\n  Troubleshooting:")
        print("  1. Make sure your .env file is correctly configured")
        print("  2. Make sure you are logged in: az login")
        print("  3. Make sure your GPT-4o deployment is active in the portal")
        sys.exit(1)

    elapsed = time.time() - start

    # Print the response
    print(response.content)
    print("\n" + "-" * 65)
    print(f"  Agent    : {response.agent_name}")
    print(f"  Duration : {elapsed:.1f}s")
    print(f"  Saved to : outputs/{agent_key}/")
    print("=" * 65 + "\n")


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="AI DevTeam — Run a single agent with a given input",
        add_help=True,
    )
    parser.add_argument(
        "--agent", "-a",
        type=str,
        help="Agent to run (e.g. pm, ba, ux, architect, developer, tester, deploy, qa)",
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        help="The message or task to send to the agent",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available agents",
    )

    args = parser.parse_args()

    if args.list:
        print_agent_list()
        return

    if not args.agent:
        print("\n  ERROR: Please specify an agent with --agent <name>")
        print("  Run 'python run_agent.py --list' to see available agents.\n")
        parser.print_help()
        sys.exit(1)

    if not args.input:
        print("\n  ERROR: Please provide input with --input \"<your message>\"")
        sys.exit(1)

    run_agent(args.agent, args.input)


if __name__ == "__main__":
    main()
