# Phase 3: Agents with Tools — The Pipeline Runner

> **Phase Status:** Complete ✅
> **Prerequisites:** Phase 1 and Phase 2 must be complete. Your `.env` file must be configured and `az login` must be active.

---

## What Phase 3 Is About

In Phase 2, agents could *talk* — they received a prompt and returned a text response printed to the terminal. In Phase 3, agents can *act*. Each agent now writes structured output files to a shared workspace on disk. The pipeline runner chains all 8 agents in sequence, passing context from one to the next, and every deliverable is saved as a named Markdown file that you can open, review, and use.

This is the transition from a **chatbot chain** to a **software delivery pipeline**.

| New Capability | What It Means |
| :--- | :--- |
| **Workspace Manager** | Every requirement gets its own timestamped folder on disk |
| **Structured file output** | Each agent writes to a specific file (e.g., `01_requirements.md`) |
| **Code file extraction** | The Developer agent's code blocks are parsed and saved as individual `.py` files |
| **Context chaining** | Each agent receives the outputs of prior agents as context — not just the raw requirement |
| **Resume support** | A failed pipeline can be resumed from any agent using `--start-from` |

---

## New Files in Phase 3

```
ai_devteam/
├── tools/
│   ├── __init__.py
│   └── workspace.py          ← Workspace manager
├── run_pipeline.py            ← Full 8-agent pipeline runner
```

---

## Step 1 — Pull the Latest Code

**macOS / Linux:**
```bash
cd ~/ai_foundry_learn && git pull
cd ai_devteam && source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
cd $HOME\ai_foundry_learn; git pull
cd ai_devteam; .venv\Scripts\activate
```

---

## Step 2 — Understand the Workspace Structure

Before running the pipeline, it helps to understand what will be created. Every time you run the pipeline, a new folder is created inside `workspaces/`:

```
workspaces/
  build_a_todo_list_rest_api_20260326_110343/
    requirement.txt              ← The original requirement you provided
    00_project_charter.md        ← Project Manager output
    01_requirements.md           ← Business Analyst output
    02_ux_spec.md                ← UI/UX Designer output
    03_architecture.md           ← Architect output
    04_src/
      output.md                  ← Developer output (code in Markdown)
    05_test_plan.md              ← Tester output
    06_deployment/
      output.md                  ← Deployment Engineer output
    07_uat_report.md             ← UAT Validator output
    pipeline.log                 ← Timestamped log of every agent run
```

Each file is named with a two-digit prefix so they sort in pipeline order — you can read them top to bottom to follow the full delivery lifecycle.

---

## Step 3 — Run the Full Pipeline

**macOS / Linux:**
```bash
python3 run_pipeline.py --requirement "Build a simple todo list REST API where users can create, read, update, and delete tasks"
```

**Windows:**
```powershell
python run_pipeline.py --requirement "Build a simple todo list REST API where users can create, read, update, and delete tasks"
```

You will see each agent run in sequence, with a preview of its output and the file path where it was saved. The full pipeline takes approximately **60–90 seconds** depending on model response times.

---

## Step 4 — Inspect the Workspace

Once the pipeline completes, open the workspace folder in VS Code:

**macOS / Linux:**
```bash
code workspaces/
```

**Windows:**
```powershell
code workspaces\
```

> **Note:** If `code` is not found, open VS Code, press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows), type **"Install 'code' command in PATH"**, press Enter, then restart your terminal.

Open each file in order and observe how each agent built on the previous one. The Architect references the BA's user stories. The Developer implements the Architect's design. The Tester writes test cases against the Developer's code. The UAT Validator assesses the full deliverable against the original requirement.

---

## Step 5 — Resume a Pipeline from a Specific Agent

If the pipeline fails partway through, or if you want to regenerate output from a specific agent without re-running the full pipeline, use `--start-from` with `--requirement`:

**macOS / Linux:**
```bash
python3 run_pipeline.py \
  --requirement "Build a simple todo list REST API" \
  --workspace workspaces/<your-workspace-folder-name> \
  --start-from developer
```

**Windows:**
```powershell
python run_pipeline.py `
  --requirement "Build a simple todo list REST API" `
  --workspace workspaces\<your-workspace-folder-name> `
  --start-from developer
```

Valid agent keys for `--start-from`: `pm`, `ba`, `ux`, `architect`, `developer`, `tester`, `deploy`, `qa`

> **Important:** Always include `--requirement` when using `--workspace`. The pipeline needs the original requirement to provide context to agents.

---

## Troubleshooting

| Error | Cause | Fix |
| :--- | :--- | :--- |
| `--workspace provided but requirement.txt not found` | Passed `--workspace` without `--requirement` | Always include `--requirement` when using `--workspace` |
| `AIProjectClient has no attribute 'inference'` | SDK v2.0 breaking change | Run `pip install --upgrade azure-ai-projects openai` then `git pull` |
| `NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+` | macOS ships with LibreSSL | Harmless warning — does not affect functionality |
| Agent produces empty output | Model timeout or quota limit | Wait 30 seconds and re-run with `--start-from` |
| `code: command not found` | VS Code CLI not installed | `Cmd+Shift+P` → "Install 'code' command in PATH" in VS Code |
| `az login` expired | Azure token expired | Run `az login` again in your terminal |

---

## Key Takeaways from Phase 3

Phase 3 introduced four concepts that are fundamental to building production-grade agentic systems.

### 1. Agents That Act, Not Just Talk

The most important shift in Phase 3 is that agents moved from generating text responses to writing structured artifacts to disk. This distinction matters because it means the output of one agent becomes a persistent, reviewable input for the next — not just a string passed through memory. In a real team, a Business Analyst does not hand a verbal summary to the Architect; they hand over a written requirements document. Phase 3 models that reality.

### 2. Workspace Isolation

Every pipeline run creates its own timestamped workspace folder. This design decision has two important consequences. First, you can compare runs — if you change a system prompt and re-run, you can diff the two workspaces side by side. Second, partial re-runs are safe — you can re-run from the Developer agent without overwriting the BA's requirements or the Architect's design. This is the same principle as immutable infrastructure in DevOps.

### 3. Structured Context Passing

The pipeline runner reads each agent's output file and passes it as context to the next agent. The Architect reads the requirements before designing the system. The Developer reads the architecture before writing code. The Tester reads both the requirements and the code before writing test cases. This structured handoff is what prevents the "telephone game" problem — where each agent in a naive chain only sees the last message, not the full picture.

### 4. The Developer Agent Invented a Project Structure

When you open `04_src/output.md`, you will notice the Developer agent created a proper folder structure (`backend/app/main.py`, `backend/app/models/task.py`, `backend/app/routes/tasks.py`, `backend/app/database.py`) without being explicitly told to. This is the system prompt doing its job — the Developer's prompt instructs it to follow professional software engineering conventions, and it applied that instruction to the specific task at hand.

---

## What Phase 3 Does Not Yet Do

Phase 3 is a **linear pipeline** — agents run in a fixed sequence and no agent can send work back to a previous agent. If the Tester finds a critical bug in the Developer's code, the pipeline simply records it in the test plan and moves on. There is no mechanism for the Developer to fix the bug and re-run the Tester.

This is the limitation that Phase 4 is designed to solve.

---

## What You Have Learned Across Phases 1–3

| Phase | Core Concept | Practical Skill |
| :--- | :--- | :--- |
| **Phase 1** | Azure AI Foundry project setup | Connect Python to Foundry using SDK v2.0 keyless auth |
| **Phase 2** | Agent specialisation via system prompts | Call any named agent with a requirement and receive structured output |
| **Phase 3** | Agents with tools — workspace, file writing, pipeline chaining | Run an 8-agent pipeline that produces a complete project workspace |
| **Phase 4** *(next)* | Active orchestration with feedback loops | PM evaluates quality, routes work back, and manages the team autonomously |
| **Phase 5** *(upcoming)* | Production readiness | Tracing, monitoring, content safety, evaluation metrics |

---

## Preview: What Changes in Phase 4

Phase 4 transforms the Project Manager from a passive first step into an **active orchestrator**. Here is the fundamental difference:

| Aspect | Phase 3 (Linear Pipeline) | Phase 4 (Orchestrated Pipeline) |
| :--- | :--- | :--- |
| **Flow control** | Fixed sequence, always runs all 8 agents | PM decides which agent runs next based on output quality |
| **Error handling** | Tester records bugs, pipeline continues | Tester flags bugs → PM routes back to Developer → Developer fixes → Tester re-runs |
| **Quality gates** | None — every output is accepted | PM evaluates each output against acceptance criteria before proceeding |
| **Feedback loops** | Not possible | BA ↔ UX Designer, Architect ↔ Developer, Tester ↔ Developer, QA ↔ any agent |
| **PM's role** | Writes a project charter and steps aside | Reads every agent's output, scores it, decides next action |
| **Termination** | Always ends after 8 agents | Ends when QA signs off — or escalates to the user if a loop cannot be resolved |

### The PM as Orchestrator — How It Will Work

In Phase 4, the Project Manager agent gains three new capabilities:

**Quality Evaluation.** After each agent completes, the PM reads its output and scores it against the acceptance criteria defined by the BA. If the score is below a threshold, the PM does not proceed to the next agent — it sends the output back with specific feedback.

**Dynamic Routing.** The PM maintains a state machine that tracks which agents have run, which outputs are accepted, and which loops are in progress. Instead of a fixed sequence, the PM chooses the next agent based on the current state.

**Loop Detection.** If the same agent fails quality evaluation more than twice in a row, the PM escalates — either trying a different approach or surfacing the problem to the user with a clear explanation of what it tried and why it failed.

This is the architecture that removes you from the integrator role. In Phase 3, you are still the one who decides whether the Developer's code is good enough. In Phase 4, the PM makes that decision — and only surfaces the result to you when the full team has signed off.

The diagram below illustrates the difference between the two pipeline models:

```
Phase 3 — Linear:
User → PM → BA → UX → Arch → Dev → Test → Deploy → QA → Done

Phase 4 — Orchestrated:
User → PM ──────────────────────────────────────────────────┐
          ↓                                                  ↑
         BA ←─── (PM rejects, sends back with feedback) ────┤
          ↓                                                  │
         UX ←─── (BA requests UX clarification) ────────────┤
          ↓                                                  │
        Arch ←── (UX requests design clarification) ────────┤
          ↓                                                  │
         Dev ←── (Arch requests implementation change) ─────┤
          ↓                                                  │
        Test ──► (Bugs found → PM routes back to Dev) ──────┤
          ↓                                                  │
       Deploy                                               │
          ↓                                                  │
          QA ──► (Fails UAT → PM routes back to Dev) ───────┘
          ↓
         Done (QA signs off → PM delivers to User)
```

---

## Next Step

When you are ready, proceed to **Phase 4: Full Team Orchestration**.

*Phase 3 complete. Your AI DevTeam now writes real files to disk and runs as a coordinated pipeline.*
