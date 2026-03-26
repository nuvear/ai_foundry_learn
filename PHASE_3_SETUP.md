# Phase 3: Agents with Tools — The Pipeline Runner

> **Prerequisites:** Phase 1 and Phase 2 must be complete. Your `.env` file must be configured and `az login` must be active.

---

## What You Will Build in Phase 3

In Phase 2, each agent could respond to a question — but every response was just printed to the terminal and saved as a JSON log. In Phase 3, the agents gain **tools**: the ability to write structured files to disk, read prior agents' outputs as context, and pass that context forward to the next agent in the pipeline.

By the end of Phase 3, a single command will trigger all 8 agents in sequence, and a complete project workspace will be written to disk — including a project charter, requirements document, UX specification, architecture document, source code files, test plan, deployment configuration, and UAT report.

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
│   └── workspace.py          ← NEW: Workspace manager
├── run_pipeline.py            ← NEW: Full 8-agent pipeline runner
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
  build_a_todo_list_rest_api_20240101_120000/
    requirement.txt           ← The original requirement you provided
    00_project_charter.md     ← Project Manager output
    01_requirements.md        ← Business Analyst output
    02_ux_spec.md             ← UI/UX Designer output
    03_architecture.md        ← Architect output
    04_src/                   ← Developer output (actual code files)
      main.py
      models.py
      database.py
    05_test_plan.md           ← Tester output
    06_deployment/            ← Deployment Engineer output
      Dockerfile
      docker-compose.yml
    07_uat_report.md          ← UAT Validator output
    pipeline.log              ← Timestamped log of every agent run
```

**Key insight:** The Developer agent's response is parsed for code blocks with filenames (e.g., `### main.py` followed by a Python code block). Each one is saved as a separate file inside `04_src/`. This is how the pipeline moves from text generation to actual file creation.

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

You will see each agent run in sequence, with a preview of its output and the file path where it was saved. The full pipeline takes approximately **2–4 minutes** depending on model response times.

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

Explore the files. Notice how each agent's output builds on the previous one — the Architect references the BA's user stories, the Developer implements the Architect's design, and the Tester writes test cases against the Developer's code.

---

## Step 5 — Resume a Pipeline from a Specific Agent

If the pipeline fails partway through (e.g., a network timeout), you do not need to start over. Use `--start-from` to resume from any agent:

**macOS / Linux:**
```bash
# Resume from the tester step in an existing workspace
python3 run_pipeline.py \
  --workspace workspaces/build_a_todo_list_rest_api_20240101_120000 \
  --start-from tester
```

**Windows:**
```powershell
python run_pipeline.py `
  --workspace workspaces\build_a_todo_list_rest_api_20240101_120000 `
  --start-from tester
```

Available agent keys for `--start-from`:

| Key | Agent |
| :--- | :--- |
| `project_manager` | Project Manager |
| `business_analyst` | Business Analyst |
| `ux_designer` | UI/UX Designer |
| `architect` | Architect |
| `developer` | Solution Developer |
| `tester` | Tester |
| `deployment_engineer` | Deployment Engineer |
| `uat_validator` | QA / UAT Validator |

---

## Step 6 — Run a Single Agent with Context

You can still use `run_agent.py` from Phase 2 to call a single agent. In Phase 3, the key difference is that the pipeline runner passes structured context — if you call an agent directly, it only receives the input you provide.

```bash
# macOS / Linux
python3 run_agent.py --agent architect --input "Build a REST API for a task manager"

# Windows
python run_agent.py --agent architect --input "Build a REST API for a task manager"
```

---

## What You Learned in Phase 3

| Concept | What You Built |
| :--- | :--- |
| **Tool use** | Agents now write files — not just text responses |
| **Context chaining** | Each agent receives prior agents' outputs as structured context |
| **Code extraction** | The Developer's code blocks are parsed and saved as individual files |
| **Workspace pattern** | Every requirement gets an isolated, timestamped folder |
| **Pipeline orchestration** | 8 agents run in sequence with a single command |
| **Resume capability** | Failed pipelines can be resumed from any step |

---

## Troubleshooting

| Error | Cause | Fix |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'tools'` | Running from wrong directory | Make sure you are inside `ai_devteam/` when running the script |
| `No workspace found` | Wrong path passed to `--workspace` | Check the folder name in `workspaces/` — it includes a timestamp |
| `Agent failed: rate limit` | Too many requests in a short time | Wait 30 seconds and re-run with `--start-from` to resume |
| `No code files extracted` | Developer response did not use expected format | The raw response is saved as `04_src/output.md` — review and re-run |
| `az login` expired | Azure token expired | Run `az login` again in your terminal |

---

## What Comes Next — Phase 4

Phase 3 is a **sequential pipeline** — agents run one after another with no feedback loops. Phase 4 introduces **orchestration**: the Project Manager agent actively monitors outputs, detects failures (e.g., the Tester finds bugs), and routes work back to the Developer for fixes. This is where the team becomes truly autonomous.

---

*Phase 3 complete. Your AI DevTeam now writes real files to disk.*
