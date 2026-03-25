# Use Case Proposals

**Author:** Manus AI  
**Last Updated:** March 2026  

## How to Choose

A great hands-on project should be complex enough to exercise all five phases of the syllabus (Model Deployment, RAG, Agents, Observability), yet concrete enough to be finished and genuinely useful. The three proposals below are designed with exactly that balance in mind. Each one will teach the same core Microsoft AI Foundry skills, but through a different real-world lens.

---

## Option A: Enterprise Document Intelligence Assistant

**Tagline:** *"Ask questions about your company's documents in plain English."*

This project builds an AI assistant that can ingest a corpus of documents (PDFs, Word files, policy manuals, technical specs) and answer natural-language questions about them with precise, cited answers. It is the most common and immediately practical AI use case in the enterprise world.

| Aspect | Detail |
| :--- | :--- |
| **Core Problem** | Knowledge is locked in PDFs and documents that are hard to search. |
| **What We Build** | A RAG-powered chat interface backed by Azure AI Search and a deployed LLM. |
| **Agent Capability** | An agent that can summarize, compare, and extract structured data from documents on demand. |
| **Foundry Features Exercised** | Model Catalog, RAG/Vector Search, Foundry IQ, Agent Service, Content Safety. |
| **Complexity** | Beginner–Intermediate |

---

## Option B: AI-Powered Code Review & Developer Copilot

**Tagline:** *"An AI pair programmer that knows your codebase."*

This project builds a developer assistant that is grounded in a specific GitHub repository. It can answer questions about the codebase, suggest code improvements, explain functions, and generate unit tests. This is highly relevant for developers who want to see AI Foundry applied to software engineering workflows.

| Aspect | Detail |
| :--- | :--- |
| **Core Problem** | Onboarding to a large codebase is slow; code reviews are time-consuming. |
| **What We Build** | An agent grounded in a GitHub repo that can explain code, suggest fixes, and write tests. |
| **Agent Capability** | An agent with tools to read files from GitHub, run static analysis, and post comments. |
| **Foundry Features Exercised** | Model Catalog, RAG (code embeddings), Agent Service, MCP (GitHub tool), Observability. |
| **Complexity** | Intermediate |

---

## Option C: Multi-Agent Research & Report Writer

**Tagline:** *"Give it a topic. Get back a structured research report."*

This project builds a multi-agent pipeline where one agent searches the web and gathers information, a second agent synthesizes and fact-checks the content, and a third agent formats the final output as a structured Markdown or Word report. This is the most advanced option and directly exercises multi-agent orchestration.

| Aspect | Detail |
| :--- | :--- |
| **Core Problem** | Research and report writing is slow and repetitive. |
| **What We Build** | A three-agent pipeline: Researcher → Analyst → Writer. |
| **Agent Capability** | Agents with web search, summarization, and document generation tools. |
| **Foundry Features Exercised** | Model Catalog, Multi-Agent Orchestration, MCP, Agent Monitoring, Evaluation. |
| **Complexity** | Intermediate–Advanced |

---

## Your Choice

Please review the three options above and let Manus know which one resonates with you — or propose your own use case entirely. Once a use case is selected, we will create a detailed project plan and start with **Phase 1: Foundation & Setup**.
