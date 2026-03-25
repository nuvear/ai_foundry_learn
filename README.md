# Microsoft AI Foundry: Hands-On Project Builder Syllabus

**Author:** Manus AI  
**Last Updated:** March 2026  

## Overview

This syllabus is designed for developers who prefer **learning by building**. We are stripping away the theory-heavy certification tracks in favor of a 100% hands-on, project-driven approach to mastering **Microsoft AI Foundry**. 

Instead of isolated labs, we will build a complete, production-ready AI application from scratch. As we build each feature, we will naturally learn the corresponding Microsoft AI Foundry capabilities—from deploying models and building agents to implementing Retrieval-Augmented Generation (RAG) and observability. I (Manus) will act as your pair programmer, providing code support, debugging, and architectural guidance along the way.

## The Learning Strategy: "Learn as You Build"

Our learning journey is structured around the software development lifecycle of a single, comprehensive AI project.

| Phase | Development Stage | AI Foundry Skills Acquired |
| :--- | :--- | :--- |
| **Phase 1** | Project Initialization & Infrastructure | Navigating the Foundry Portal, setting up projects, Role-Based Access Control (RBAC). |
| **Phase 2** | Core Intelligence (The "Brain") | Deploying models from the Model Catalog (OpenAI, DeepSeek, etc.), using the Foundry SDK (Python/C#). |
| **Phase 3** | Knowledge Integration (The "Memory") | Implementing RAG, vector search, and Foundry IQ to ground the AI in custom enterprise data. |
| **Phase 4** | Agentic Workflows (The "Hands") | Using the Foundry Agent Service, Model Context Protocol (MCP), and multi-agent orchestration to perform actions. |
| **Phase 5** | Production Readiness (The "Guardrails") | Implementing tracing (OpenTelemetry), Agent Monitoring Dashboard, and Azure AI Content Safety. |

---

## Phase 1: Foundation & Setup

Before writing code, we need a solid foundation. In this phase, we will set up our cloud environment and establish our local development workspace.

| Task | Description |
| :--- | :--- |
| **Environment Setup** | Create an Azure account and deploy a new Microsoft AI Foundry project workspace. |
| **Local Workspace** | Initialize a local Git repository, set up a Python/C# virtual environment, and install the `azure-ai-projects` and `azure-ai-inference` SDKs. |
| **Authentication** | Configure Azure CLI and set up secure, keyless authentication (DefaultAzureCredential) for local development. |

---

## Phase 2: Core Intelligence (Model Deployment)

An AI application needs a brain. We will explore the Model Catalog and write our first lines of code to interact with a Large Language Model (LLM).

| Task | Description |
| :--- | :--- |
| **Model Selection** | Browse the Foundry Model Catalog and deploy a foundation model (e.g., GPT-4o or DeepSeek-R1) as a serverless API endpoint. |
| **Basic Inference** | Write a simple script using the Foundry SDK to send a prompt to the deployed model and receive a response. |
| **System Prompts** | Learn how to craft system prompts to define the persona, tone, and boundaries of our AI application. |

---

## Phase 3: Knowledge Integration (RAG & Foundry IQ)

LLMs only know what they were trained on. To make our application useful, we need to give it access to custom data without retraining the model.

| Task | Description |
| :--- | :--- |
| **Data Ingestion** | Upload sample project data (documents, PDFs, or code) to Azure Blob Storage. |
| **Vector Indexing** | Create an Azure AI Search resource and generate vector embeddings for our custom data. |
| **Implementing RAG** | Modify our inference code to query the search index first, retrieve relevant context, and append it to the prompt before sending it to the LLM. |
| **Foundry IQ (Optional)** | Explore using Foundry IQ as an enterprise intelligence layer to connect directly to SharePoint or OneLake. |

---

## Phase 4: Agentic Workflows & Tools

An AI that only chats is limited. We will upgrade our application into an "Agent" that can take actions, use tools, and execute multi-step workflows.

| Task | Description |
| :--- | :--- |
| **Defining Tools** | Create Python/C# functions that perform specific tasks (e.g., querying a database, fetching weather, or calling an external API). |
| **Agent Orchestration** | Use the Foundry Agent Service to bind our deployed model with the tools we created. |
| **Model Context Protocol (MCP)** | Implement an MCP server to standardize how our agent interacts with external tools and data sources. |
| **Multi-Agent Setup** | (Advanced) Create a workflow where two different agents (e.g., a "Researcher" and a "Writer") collaborate to solve a complex task. |

---

## Phase 5: Observability & Content Safety

Before calling a project "done," we must ensure it is safe, reliable, and easy to debug.

| Task | Description |
| :--- | :--- |
| **Tracing** | Integrate OpenTelemetry into our code to log every LLM call, tool execution, and latency metric to the Foundry portal. |
| **Monitoring Dashboard** | Navigate the Agent Monitoring Dashboard in Foundry to visualize token usage and execution traces. |
| **Content Safety** | Implement Azure AI Content Safety guardrails to automatically detect and block jailbreak attempts, hate speech, or sensitive data leaks. |
| **Evaluation** | Run automated evaluations against our RAG implementation to measure relevance, groundedness, and completeness. |

---

## Next Steps: Choose Your Use Case

To begin, we need to define **what** we are building. The best projects are ones that solve a real problem or align with your interests. 

*(See the discussion thread to select a use case, or propose your own!)*
