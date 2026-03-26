# Phase 2: Core Intelligence — Building the Agent Brains

**Project:** AI DevTeam  
**Phase:** 2 of 5  
**Prerequisite:** Phase 1 complete — Azure connected, GPT-4o responding  
**Language:** Python 3.9+

---

## What You Will Build

In Phase 2 you create the foundation that all 8 AI agents are built on. By the end of this phase, you can call any individual agent from the command line and receive a structured, professional output.

| What Gets Built | What You Learn |
| :--- | :--- |
| `BaseAgent` class | How to structure reusable AI agent code |
| 8 system prompt files | How system prompts define agent behaviour and output format |
| 8 agent classes | How to specialise a base class for different roles |
| `run_agent.py` CLI runner | How to invoke a specific agent with a task |
| `shared/config.py` (updated) | How to manage configuration across a multi-agent project |

---

## New Files in This Phase

```
ai_devteam/
├── agents/
│   ├── __init__.py            ← Agent registry (maps CLI names to classes)
│   ├── base_agent.py          ← BaseAgent class (all agents inherit from this)
│   ├── project_manager.py     ← Agent 1: PM / Orchestrator
│   ├── business_analyst.py    ← Agent 2: Business Analyst
│   ├── ux_designer.py         ← Agent 3: UI/UX Designer
│   ├── architect.py           ← Agent 4: Architect
│   ├── developer.py           ← Agent 5: Solution Developer
│   ├── tester.py              ← Agent 6: Tester
│   ├── deployment_engineer.py ← Agent 7: Deployment Engineer
│   └── uat_validator.py       ← Agent 8: QA / UAT Validator
├── prompts/
│   ├── project_manager.txt
│   ├── business_analyst.txt
│   ├── ux_designer.txt
│   ├── architect.txt
│   ├── developer.txt
│   ├── tester.txt
│   ├── deployment_engineer.txt
│   └── uat_validator.txt
├── run_agent.py               ← CLI runner for single-agent testing
└── shared/
    └── config.py              ← Updated: adds OUTPUTS_DIR, singleton pattern
```

---

## Step 1 — Pull the Latest Code

```bash
cd ~/ai_foundry_learn
git pull
cd ai_devteam
```

---

## Step 2 — Activate Your Virtual Environment

```bash
source .venv/bin/activate
```

Your prompt should show `(.venv)` at the start.

---

## Step 3 — Install New Dependencies

Phase 2 uses the same packages as Phase 1. No new installs required.
Verify everything is still installed:

```bash
pip install -r requirements.txt
```

---

## Step 4 — List Available Agents

```bash
python run_agent.py --list
```

Expected output:

```
Available Agents:
-----------------------------------------------------------------
  Key          Agent Name             Produces
-----------------------------------------------------------------
  pm           Project Manager        Creates Project Charter, orchestrates the pipeline
  ba           Business Analyst       Produces FRD, User Stories, Acceptance Criteria
  ux           UI/UX Designer         Wireframes, User Flows, Component Specifications
  architect    Architect              HLD, Tech Stack, API Contracts, Data Models
  developer    Solution Developer     Source Code, Unit Tests, README
  tester       Tester                 Test Plan, Test Cases, Bug Reports
  deploy       Deployment Engineer    Dockerfile, CI/CD Pipeline, Deployment Guide
  qa           QA / UAT Validator     UAT Scenarios, Final Sign-off
```

---

## Step 5 — Run Your First Agent

Start with the Project Manager — give it a simple requirement:

```bash
python run_agent.py --agent pm --input "Build a simple todo list web app where users can add, complete, and delete tasks"
```

The PM will respond with a structured **Project Charter** including scope, deliverables, agent pipeline, and risk assessment.

---

## Step 6 — Try Each Agent

Work through the pipeline manually, passing the output of one agent as input to the next.

**Business Analyst** (give it the same requirement):
```bash
python run_agent.py --agent ba --input "Build a simple todo list web app where users can add, complete, and delete tasks"
```

**UI/UX Designer** (give it the BA's User Stories):
```bash
python run_agent.py --agent ux --input "We are building a todo list app. User stories: US-1: As a user, I want to add a task so I can track my work. US-2: As a user, I want to mark a task complete. US-3: As a user, I want to delete a task."
```

**Architect** (give it the FRD summary):
```bash
python run_agent.py --agent architect --input "Build a todo list web app. Frontend: React. Backend: FastAPI. Database: SQLite for local dev. Single user, no auth required for MVP."
```

**Developer** (give it the HLD):
```bash
python run_agent.py --agent developer --input "Implement a FastAPI backend with endpoints: GET /tasks, POST /tasks, PATCH /tasks/{id}/complete, DELETE /tasks/{id}. Use SQLite with SQLAlchemy. Return JSON."
```

---

## Understanding the Code

### How BaseAgent Works

Every agent follows the same pattern:

```
1. Load system prompt from prompts/<role>.txt
2. Connect to Foundry using DefaultAzureCredential (keyless auth)
3. Build messages: [SystemMessage] + [history] + [UserMessage]
4. Call the model via chat completions
5. Save the response to outputs/<role>/<timestamp>.json
6. Return an AgentResponse object
```

### Why Different Temperatures?

Each agent uses a different `temperature` setting:

| Agent | Temperature | Why |
| :--- | :--- | :--- |
| PM | 0.5 | Balanced — structured but not robotic |
| BA | 0.5 | Balanced — precise but readable |
| UX Designer | 0.7 | Higher — creative design decisions |
| Architect | 0.4 | Lower — precise technical choices |
| Developer | 0.3 | Lowest — deterministic, correct code |
| Tester | 0.3 | Lowest — consistent test reports |
| Deploy Engineer | 0.3 | Lowest — precise infrastructure code |
| QA / UAT | 0.5 | Balanced — user-perspective judgement |

### Where Outputs Are Saved

Every agent interaction is automatically saved to:
```
ai_devteam/outputs/<agent_role>/<timestamp>.json
```

This gives you a full audit trail of every agent's work — useful for debugging and for Phase 4 when agents need to read each other's outputs.

---

## Troubleshooting

| Error | Cause | Fix |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'agents'` | Not running from the `ai_devteam/` directory | `cd ~/ai_foundry_learn/ai_devteam` then retry |
| `EnvironmentError: Missing required environment variables` | `.env` file not found or incomplete | Check `.env` exists and all 4 variables are set |
| `DefaultAzureCredential: No credential found` | Not logged in to Azure CLI | Run `az login` |
| `ResourceNotFoundError` | Model deployment name is wrong | Check the exact name in the Foundry portal |
| `AuthenticationError` | Token expired | Run `az login` again |

---

## What You Learned in Phase 2

By completing this phase, you have learned:

**Foundry SDK patterns** — how `AIProjectClient` and `get_chat_completions_client()` work together to call a deployed model.

**System prompt engineering** — how a well-crafted system prompt defines an agent's role, output format, and decision-making principles. The difference between a generic chatbot and a specialist agent is almost entirely in the system prompt.

**Agent architecture** — the BaseAgent pattern: one class handles all the infrastructure (connection, history, logging), and subclasses only define what makes each agent unique (name, role, prompt, temperature).

**Conversation history** — how multi-turn conversations work: each call appends to a history list, and the full history is sent with every new message so the agent remembers context.

**Temperature as a design decision** — lower temperature = more deterministic and consistent; higher temperature = more creative and varied. Different tasks need different settings.

---

## Next: Phase 3 — First Agent with Tools

In Phase 3, we upgrade the Solution Developer agent from a "thinking" agent to an "acting" agent by giving it tools: the ability to write files, run code, and interact with the file system. This is where agents stop just talking and start doing.
