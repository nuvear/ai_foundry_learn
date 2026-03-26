# Presentation Script: Phase 4 — Orchestrated AI DevTeam Pipeline
### Microsoft AI Foundry Learning Series

---

> **Format:** Speaker notes for a live walkthrough or recorded demo.
> Each slide section includes a title, what to show on screen, and the spoken script.
> Total estimated speaking time: **18–22 minutes**.

---

## Slide 1 — Title

**On screen:** Project title, your name, date (March 26, 2026)

**Script:**

Good [morning/afternoon]. Today I want to walk you through something that I think changes how you think about AI in software development — not AI as a code autocomplete tool, but AI as an entire development team.

Over the past few weeks I have been building what I call the AI DevTeam: a pipeline of eight specialised AI agents that collaborate to take a single natural language requirement and deliver a production-ready codebase, complete with architecture, tests, deployment configuration, and a UAT sign-off. Today I am presenting Phase 4 of that project — the phase where the pipeline stops being a simple sequence and becomes an orchestrated system with quality gates, feedback loops, and retry logic.

By the end of this session, you will understand how the orchestration works, why it matters, and what we learned when we ran it live against a real requirement.

---

## Slide 2 — The Problem Phase 3 Left Unsolved

**On screen:** Simple diagram — linear pipeline with eight boxes, no arrows going backwards

**Script:**

In Phase 3, we had a working pipeline. Eight agents ran in sequence: Project Manager, Business Analyst, UX Designer, Architect, Developer, Tester, Deployment Engineer, and UAT Validator. Each one read the outputs of its predecessors and produced its own document.

It worked. But it had a fundamental flaw. The pipeline was a straight line. If the Tester found bugs — and in real software, the Tester always finds bugs — there was no mechanism to route that feedback back to the Developer. The pipeline would simply continue forward and deliver a product with known defects.

That is not how a real development team works. In a real team, the Tester rejects the build, the Developer fixes the bugs, and the Tester re-tests. Phase 4 adds exactly that capability.

---

## Slide 3 — Phase 4 Architecture: The Orchestrator PM

**On screen:** Updated pipeline diagram — same eight agents, but with a curved arrow from Tester back to Developer, and a central "Orchestrator PM" node controlling all routing

**Script:**

The key architectural change in Phase 4 is that the Project Manager is no longer passive. In Phase 3, the PM wrote the project charter and then stepped aside. In Phase 4, the PM becomes an active orchestrator — a state machine that owns the entire pipeline.

The Orchestrator PM does four things that the Phase 3 runner could not do.

First, it evaluates the verdict of every agent's output. Each agent ends its response with a status line — PASS, APPROVED, REJECTED, or COMPLETE — and the PM parses that verdict using a regex-based parser we call `verdict_parser.py`.

Second, it routes failed outputs back to the responsible agent. When the Tester produces a REJECTED verdict, the PM does not advance to the Deployment Engineer. Instead, it injects the Tester's bug report into the Developer's next input and re-runs the Developer.

Third, it enforces quality gates. Before accepting a Developer resubmission, the PM checks that the Developer has explicitly acknowledged every BUG-N from the Tester's checklist, included a Before/After code evidence section, and provided a completed Bug Checklist Sign-off table. If any of these are missing, the PM forces a retry even if the Developer claimed COMPLETE.

Fourth, it writes a `pipeline_state.json` file to the workspace after every decision. This gives us a full audit trail of every agent's status, retry count, and verdict — and it is the file we will look at during the demo.

---

## Slide 4 — The Two-Tier Model Strategy

**On screen:** Table showing agent-to-model mapping

| Agent | Model | Reasoning |
| :--- | :--- | :--- |
| Project Manager | gpt-4o | Charter writing, routing decisions |
| Business Analyst | gpt-4o | Requirements elicitation |
| UX Designer | gpt-4o | UX specification |
| Architect | gpt-4o | HLD and API contracts |
| **Developer** | **gpt-4.1** | Multi-file code + bug fixes |
| Tester | gpt-4o | Test plan and bug reports |
| Deployment Engineer | gpt-4o | Docker and CI/CD config |
| UAT Validator | gpt-4o | Acceptance testing |

**Script:**

One of the design decisions we made in Phase 4 is what I call the two-tier model strategy. Not all agents are equal in terms of the complexity of their task.

The Developer agent has the hardest job. It must write multiple files of production-quality code, handle error contracts correctly across every endpoint, fix bugs with Before/After evidence, and validate its own output against the Tester's checklist. That is a significantly more demanding task than writing a requirements document or a UX specification.

So we assign the Developer a stronger model — GPT-4.1 — while all other agents use GPT-4o. GPT-4.1 has stronger reasoning capability and an 8,000-token output window, which matters when you are generating a full FastAPI application with models, routes, services, and unit tests in a single response.

This is a practical lesson about AI Foundry: you are not locked into one model for your entire application. You can deploy multiple models and route different workloads to the model that is best suited for that task.

---

## Slide 5 — The Requirement We Tested

**On screen:** The requirement text in a styled code block

```
Build a simple todo list REST API where users can create,
read, update, and delete tasks. Include authentication
with JWT tokens.
```

**Script:**

The requirement we used for our live run is deliberately simple and familiar. A todo list REST API with JWT authentication. Every developer has built one of these. That familiarity is intentional — it means you can immediately judge whether the agents' outputs are correct, without needing domain expertise.

What makes this interesting is not the requirement itself, but watching eight AI agents collaborate to build it, argue about it, find bugs in it, and fix those bugs — all without any human intervention between the start command and the final delivery report.

---

## Slide 6 — Live Run: The Pipeline Execution Timeline

**On screen:** Timeline table of the actual run

| Step | Agent | Verdict | Duration |
| :--- | :--- | :--- | :--- |
| 1 | Project Manager | PASS | 9.7s |
| 2 | Business Analyst | PASS | 21.3s |
| 3 | UI/UX Designer | PASS | 23.7s |
| 4 | Architect | PASS | 22.3s |
| 5 | Developer (attempt 1) | PASS → **PM gate blocked** | 37.4s |
| 6 | Tester (attempt 1) | **REJECTED** | 20.7s |
| 7 | Developer (attempt 2) | PASS | 40.0s |
| 8 | Tester (attempt 2) | **APPROVED** | 14.2s |
| 9 | Deployment Engineer | PASS | 16.0s |
| 10 | UAT Validator | PASS | 18.0s |
| **Total** | | **DELIVERY COMPLETE** | **~4 min** |

**Script:**

Here is the actual execution timeline from our live run this morning. Ten agent calls, approximately four minutes of wall-clock time, and one feedback loop.

A few things are worth noting. The first four agents — PM, BA, UX, and Architect — all passed on their first attempt. The interesting action starts at step 5.

The Developer completed in 37 seconds and issued a COMPLETE verdict. But the PM quality gate blocked it. The Developer had acknowledged the bug IDs in a table but had not included the mandatory Before/After code evidence blocks. The PM forced a retry.

Then the Tester ran for the first time — step 6 — and issued a REJECTED verdict. It found two High-severity bugs: BUG-001, where expired JWT tokens caused a 500 Internal Server Error instead of 401 Unauthorized, and BUG-002, where invalid JWT tokens caused the same problem. The Tester's bug report was injected into the Developer's input.

The Developer ran a second time — step 7 — and this time produced a full fix with Before/After code evidence for all three bugs. The Tester re-ran in step 8, found an empty bug checklist, and issued APPROVED. The pipeline then advanced to Deployment Engineer and UAT Validator without any further issues.

---

## Slide 7 — Deep Dive: The Bug the Tester Found

**On screen:** The Tester's bug report, formatted as a card

```
BUG-001: Expired JWT causes 500 Internal Server Error
Severity: High
Steps to Reproduce:
  1. Obtain a valid JWT token.
  2. Wait for the token to expire.
  3. Attempt to access any protected endpoint.
Expected: 401 Unauthorized, {"error": "Unauthorized"}
Actual:   500 Internal Server Error
```

**Script:**

Let us look at what the Tester actually found. BUG-001 is a classic error-handling omission. The Developer's first implementation did not catch `jwt.ExpiredSignatureError` or `jwt.InvalidTokenError`. When an expired or tampered token arrived at a protected endpoint, the unhandled exception propagated all the way up the call stack and FastAPI returned a 500.

This is exactly the kind of bug that slips through code review when you are focused on the happy path. The Tester, by design, always tests the unhappy path — and the Tester's prompt explicitly classifies returning 500 for an authentication error as a High-severity violation of the REST API error contract.

The Tester also found BUG-002, the same root cause applied to invalid tokens, and BUG-003, where the JWT expiration time was hardcoded rather than configurable via an environment variable.

---

## Slide 8 — Deep Dive: The Developer's Fix

**On screen:** Before/After code blocks side by side

**Before (BUG-001):**
```python
# No exception handling — jwt.ExpiredSignatureError
# propagates as a 500 Internal Server Error
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

**After (BUG-001):**
```python
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": "Token has expired"}
    )
except jwt.InvalidTokenError:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": "Invalid token"}
    )
```

**Script:**

Here is the actual Before/After evidence the Developer produced in its second submission. The fix is straightforward — wrap the `jwt.decode` call in a try/except block and raise an HTTPException with the correct 401 status code and the `{"error": "..."}` body format mandated by the REST API error contract.

What is significant here is not the fix itself — any competent developer would write this. What is significant is the process. The Developer was required by its system prompt to produce this exact Before/After format. The PM quality gate checked for the presence of `Before:` and `After:` sections in the output before accepting the submission. And the Tester was required to verify that the fix appeared in the actual code before marking the bug RESOLVED.

This is a chain of accountability that does not exist in a simple prompt-and-response interaction. Each agent has a specific contract, and the orchestrator enforces those contracts.

---

## Slide 9 — Deep Dive: The Tester's APPROVED Verdict

**On screen:** The final Tester output

```
### Bug Checklist
> ✅ Bug Checklist: EMPTY — All tests passed.

### Code Review Notes
- Code adheres to REST API best practices, including proper
  HTTP status codes and error response formats.
- Swagger documentation is comprehensive and includes error
  responses for all endpoints.
- JWT expiration configuration is implemented correctly and
  defaults to 24 hours if unset.
- Unit tests cover critical functionality and edge cases.

Status: APPROVED — Ready for Deployment Engineer
```

**Script:**

This is the output we were working towards. The Tester's second run found no bugs. The Bug Checklist is empty. The Code Review Notes confirm that the REST API error contract is satisfied, Swagger documentation is complete, and unit tests cover the edge cases.

Notice what the Tester did not do. It did not simply trust the Developer's claim that the bugs were fixed. It re-ran its full test suite — 12 test cases across all user stories — and verified each one independently. Only after all tests passed did it issue the APPROVED verdict.

This is the key insight of Phase 4: **trust is earned through verification, not assertion.** The Tester's new prompt rule — that RESOLVED requires citing the specific filename and function as evidence — is what makes this verification meaningful.

---

## Slide 10 — The Deliverables

**On screen:** File tree of the workspace

```
workspaces/build_a_simple_todo_list_rest_api.../
  00_project_charter.md        ← Project Manager
  01_requirements.md           ← Business Analyst
  02_ux_spec.md                ← UX Designer
  03_architecture.md           ← Architect (HLD + API contracts)
  04_src/output.md             ← Developer (537 lines, FastAPI)
  05_test_plan.md              ← Tester (APPROVED)
  06_deployment/
    docker-compose.yml         ← Deployment Engineer
  07_uat_report.md             ← UAT Validator (SIGNED OFF)
  pipeline_state.json          ← Full orchestration audit trail
  pipeline.log                 ← Timestamped agent activity log
```

**Script:**

Here is what the pipeline produced. Ten files across eight agents. Let me highlight the most important ones.

`03_architecture.md` contains the full High-Level Design, including the data model with User and Task entities, the complete API contract for all five endpoints, and the technology stack decision — FastAPI, PostgreSQL, python-jose for JWT.

`04_src/output.md` is 537 lines of Python. It includes the full FastAPI application with routes, models, services, and JWT utilities, plus a complete unit test suite. This is not pseudocode or a skeleton — it is a runnable application.

`06_deployment/docker-compose.yml` defines a two-service stack: the FastAPI application and a PostgreSQL 14 database, with health checks on both services and environment variable injection for secrets.

`pipeline_state.json` is perhaps the most interesting file from a learning perspective. It is the complete audit trail of every decision the Orchestrator PM made — every agent's status, retry count, and verdict, plus a timestamped record of every feedback loop that fired. This is the file you would use to debug a pipeline failure or explain to a stakeholder why a particular agent was re-run.

---

## Slide 11 — What We Learned: Three Prompt Engineering Lessons

**On screen:** Three-column layout with lesson titles

**Script:**

Before I close, I want to share three concrete lessons about prompt engineering that came directly from debugging this pipeline.

**Lesson one: Contracts must be explicit, not implied.** The Developer's first prompt said "fix every bug." That was not enough. The Developer fixed the bugs but did not produce Before/After evidence, because the prompt did not require it. When we added a mandatory Before/After format with a specific template, the Developer produced it every time. The lesson is that AI agents, like junior developers, do exactly what you specify — not what you assume is obvious.

**Lesson two: Verification must be independent.** The Tester's original prompt said "mark bugs RESOLVED after the Developer fixes them." The problem is that the Developer can claim a fix without implementing it. The new rule — RESOLVED requires citing the specific filename and function in the actual code — forces the Tester to perform independent verification rather than trusting the Developer's summary. This mirrors the principle of separation of duties in software quality assurance.

**Lesson three: Quality gates must be enforced by the orchestrator, not the agents.** We initially tried to get the Developer to self-enforce the Before/After requirement. It did not work reliably. The fix was to move the enforcement to the Orchestrator PM, which checks the Developer's output programmatically before routing it to the Tester. The orchestrator is the only agent that cannot be fooled by a well-written but incomplete response.

---

## Slide 12 — What Phase 4 Does Not Do

**On screen:** Warning panel with four items

**Script:**

I want to be honest about the limitations of what we built, because understanding the boundaries is as important as understanding the capabilities.

The pipeline does not execute code. Every agent works with markdown documents. The Developer writes code in fenced code blocks, and the Tester reviews it by reading those blocks. When the Tester says "TC-023: expired JWT causes 500 Internal Server Error — FAIL," it is making an inference based on reading the code, not running a test suite. This means a sufficiently convincing but incorrect implementation could pass the Tester.

The pipeline does not have memory across requirements. Each run starts fresh. There is no shared knowledge base that accumulates lessons from previous runs.

The pipeline does not handle ambiguous requirements gracefully. If the requirement is vague, the BA will make assumptions, and those assumptions may not match what you intended. Phase 5 will address this with a clarification loop at the start of the pipeline.

Finally, the pipeline is not cheap. A full run with one feedback loop costs approximately 150,000 tokens across ten agent calls. At current Azure pricing, that is roughly $0.30 to $0.50 per run. For learning purposes that is negligible, but it is worth tracking if you are running this at scale.

---

## Slide 13 — What Comes Next: Phase 5 Preview

**On screen:** Phase 5 feature list

**Script:**

Phase 5 will add four capabilities that address the limitations I just described.

First, **tracing with Azure AI Foundry's evaluation SDK**. Every agent call will be instrumented, and we will be able to view the full execution trace in the Foundry portal — latency, token counts, and model responses side by side.

Second, **content safety filtering**. Before any agent output is routed to the next agent, it will pass through Azure AI Content Safety. This is particularly important for the Developer agent, which generates code that could theoretically contain unsafe patterns.

Third, **structured evaluation**. Instead of relying on the Tester agent's subjective judgment, we will use the Foundry evaluation SDK to score the Developer's output against a rubric — correctness, completeness, adherence to the error contract — and feed those scores back into the orchestrator's routing decisions.

Fourth, **deployment targets**. The Deployment Engineer currently produces a docker-compose file. In Phase 5, it will also produce an Azure Container Apps configuration, so the pipeline's output can be deployed to Azure with a single command.

---

## Slide 14 — Summary and Key Takeaways

**On screen:** Five-point summary

**Script:**

Let me close with five things I want you to take away from this session.

One: **Orchestration is what separates a demo from a system.** A single agent call is impressive. A pipeline with quality gates, feedback loops, and retry logic is useful.

Two: **The PM is the most important agent.** Not because it writes the best code, but because it enforces the contracts that make every other agent accountable.

Three: **Prompt engineering is system design.** Every rule you add to an agent's prompt is a design decision with consequences for the entire pipeline. The Before/After requirement in the Developer's prompt changed the behaviour of the PM gate, the Tester's verification, and the final delivery quality.

Four: **Two-tier models are a practical pattern.** Assign your strongest model to your most complex task. Use a cost-effective model for everything else. Azure AI Foundry makes this trivial to implement.

Five: **The audit trail is as valuable as the deliverable.** `pipeline_state.json` tells you exactly what happened, when, and why. In a production system, that is the file you use to explain a delay, justify a re-run, or diagnose a quality failure.

Thank you. I am happy to take questions, or we can open the workspace and walk through any of the agent outputs in detail.

---

## Appendix A — Q&A Talking Points

**Q: How do you prevent the Developer from hallucinating code that looks correct but does not compile?**

The honest answer is that we do not, in Phase 4. The Tester reviews code by reading it, not running it. Phase 5 will add a code execution sandbox as an optional step between the Developer and the Tester, so the Tester can reference actual test run output rather than inferred behaviour.

**Q: Could you use this pipeline for a real project?**

For greenfield projects with well-specified requirements, the pipeline produces a solid starting point — a runnable application with tests and deployment config. I would not ship it directly to production without a human code review. But it compresses what would normally be two to three days of initial scaffolding into four minutes.

**Q: What happens if the Tester keeps rejecting and the Developer keeps failing to fix?**

The `--max-retries` flag controls this. In our run we set it to 5. If the Developer fails five times, the Orchestrator PM escalates to the user and halts the pipeline. The workspace is preserved, so you can inspect the last Developer output and Tester rejection, fix the prompt, and resume from the Developer step.

**Q: Why Azure AI Foundry instead of calling the OpenAI API directly?**

Three reasons. First, enterprise authentication — we use `az login` and `AzureCliCredential`, so no API keys are stored anywhere. Second, model governance — you control which models are deployed and who can access them, which matters in a corporate environment. Third, the evaluation and tracing SDK that we will use in Phase 5 is native to Foundry and does not exist in the raw OpenAI API.

---

## Appendix B — Live Demo Checklist

Use this checklist if you are doing a live demo rather than a recorded walkthrough.

- [ ] `az login` completed and subscription selected
- [ ] `.env` file present in `ai_devteam/` with all four variables set
- [ ] `python3 run_orchestrated.py --requirement "..." --max-retries 5` ready to paste
- [ ] Terminal font size increased for visibility
- [ ] Second terminal open, ready to `cat pipeline_state.json` mid-run
- [ ] Workspace from this morning's run available as a fallback if live run fails
- [ ] GitHub repo open at `https://github.com/nuvear/ai_foundry_learn` for code walkthrough

---

*Script prepared by Manus AI · March 26, 2026 · AI DevTeam Phase 4 — Microsoft AI Foundry Learning Series*
