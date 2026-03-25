# Microsoft AI Foundry Learning Syllabus

**Author:** Manus AI  
**Last Updated:** March 2026  

## Overview

This syllabus is designed to provide a comprehensive learning path for mastering **Microsoft AI Foundry** (formerly Azure AI Studio). Microsoft AI Foundry is a unified Azure platform-as-a-service offering that combines enterprise AI operations, model building, and application development [1]. It unifies agents, models, and tools under a single management grouping with built-in enterprise-readiness capabilities, including tracing, monitoring, evaluations, and customizable enterprise setup configurations [1].

Whether you are an application developer building AI-powered products, a machine learning engineer fine-tuning models, or an IT administrator governing AI resources, this syllabus will guide you from the fundamentals to advanced topics.

## Course Objectives

By completing this syllabus, learners will gain a deep understanding of the core components and capabilities of Microsoft AI Foundry. They will be equipped to build and orchestrate AI agents using the Microsoft Foundry SDK and Agent Service, as well as integrate knowledge and ground AI models using Retrieval-Augmented Generation (RAG) and Foundry IQ. Furthermore, learners will develop the skills to fine-tune, deploy, and evaluate AI models from the Foundry Model Catalog. Finally, the course will cover the implementation of enterprise-grade security, observability, and responsible AI practices, preparing learners for the Microsoft Certified: Azure AI Engineer Associate (AI-102) exam [2].

---

## Module 1: Introduction to Microsoft AI Foundry

This module covers the basics of Microsoft AI Foundry, exploring its evolution from previous Azure AI services and outlining its core capabilities. It establishes the foundational knowledge required for subsequent modules.

| Topic | Description |
| :--- | :--- |
| **What is Microsoft AI Foundry?** | A unified platform for agents, models, and tools, representing the evolution from Azure OpenAI and Azure AI Studio [1]. |
| **Target Audiences** | Designed for Application Developers, ML Engineers, and IT Administrators [1]. |
| **Key Capabilities** | Features include building agents (Multi-agent orchestration, Tool catalog, Memory) and operating/governing (Real-time observability, Centralized AI asset management) [1]. |
| **Navigating the Portal** | Setting up projects, managing resources, and accessing the Model Catalog and integrated tools [1]. |

**Hands-on Lab:** Learners will create an Azure account, access the Microsoft Foundry Portal, create a new Foundry project, and familiarize themselves with the user interface.

---

## Module 2: Building AI Agents and Applications

This module transitions from theory to practice, teaching learners how to develop intelligent agents and applications using the Microsoft Foundry SDK and Agent Service.

| Topic | Description |
| :--- | :--- |
| **Microsoft Foundry API and SDKs** | An introduction to the unified API contract and the use of SDK client libraries across Python, C#, JavaScript, and Java [1]. |
| **Foundry Agent Service** | Techniques for developing AI agents and orchestrating multi-agent workflows [1] [2]. |
| **Integrating Tools and Memory** | Methods for connecting to the extensive tool catalog (over 1,400 tools) and implementing agent memory to maintain context during interactions [1]. |
| **Model Context Protocol (MCP)** | Strategies for integrating MCP Tools with Azure AI Agents to enhance functionality [2]. |

**Hands-on Lab:** Learners will develop a simple AI chat application using the Microsoft Foundry SDK (Python or C#) and create a multi-agent workflow that utilizes a specific tool from the catalog.

---

## Module 3: Knowledge Integration and Grounding (RAG)

This module focuses on the critical practice of grounding AI models with enterprise data. By implementing these techniques, developers can significantly reduce hallucinations and improve the accuracy of AI-generated responses.

| Topic | Description |
| :--- | :--- |
| **RAG Fundamentals** | Core concepts of indexing and grounding data to improve generative AI outputs [3]. |
| **Foundry IQ** | Exploring the enterprise intelligence layer that connects knowledge bases like SharePoint, Azure Blob Storage, and OneLake to AI agents [1] [4]. |
| **Implementing RAG** | Practical application of prompt flow for RAG and the integration of Azure AI Search within the Foundry environment [3]. |

**Hands-on Lab:** Learners will build a RAG-based solution utilizing their own data within the Foundry portal [2]. Additionally, they will configure Foundry IQ to connect an agent to an Azure Blob Storage container.

---

## Module 4: Model Customization and Deployment

In this module, learners will explore the extensive Foundry Model Catalog. They will learn the criteria for choosing between fine-tuning and RAG, as well as the technical steps required to fine-tune and deploy models for specific tasks.

| Topic | Description |
| :--- | :--- |
| **Foundry Model Catalog** | Navigating available models (including OpenAI, DeepSeek, and HuggingFace) and understanding the Models as a Service (MaaS) offering [5] [6]. |
| **Fine-Tuning Models** | Evaluating when to fine-tune versus using RAG, and executing the fine-tuning process, which requires the Azure AI Owner role [5]. |
| **Deploying Models** | Procedures for deploying fine-tuned models for inferencing and managing model deployments and endpoints [5]. |

**Hands-on Lab:** Learners will deploy a pre-trained model from the catalog and test it via API. They will also practice fine-tuning a language model using a custom dataset within the Foundry portal [2].

---

## Module 5: Observability, Evaluation, and Responsible AI

Ensuring that AI applications are safe, reliable, and performant is paramount. This module covers the built-in tools provided by Foundry to monitor and evaluate AI systems.

| Topic | Description |
| :--- | :--- |
| **Real-time Observability** | Techniques for tracing and monitoring AI agents using OpenTelemetry and the Agent Monitoring Dashboard [7]. |
| **Evaluating AI Performance** | Utilizing built-in tools to evaluate models and agents, including measuring content safety with specific evaluators [2] [8]. |
| **Responsible AI** | Implementing generative AI guardrails and leveraging Azure AI Content Safety within the Foundry Control Plane [2] [8]. |
| **Enterprise Controls** | Managing Role-Based Access Control (RBAC), networking configurations, and Azure Policy integration [1]. |

**Hands-on Lab:** Learners will configure tracing for an AI agent framework and analyze the resulting traces in the portal [7]. They will also evaluate a generative AI solution and implement appropriate content safety guardrails [2].

---

## Module 6: Certification Preparation (AI-102)

The final module is dedicated to preparing learners for the Microsoft Certified: Azure AI Engineer Associate (AI-102) exam, validating their skills in designing and implementing AI solutions.

| Topic | Description |
| :--- | :--- |
| **Exam Overview** | A comprehensive breakdown of the AI-102 exam structure, objectives, and expectations [9]. |
| **Concept Review** | A thorough review of key concepts, including designing, implementing, and integrating AI models into applications. |
| **Practice and Assessment** | Engaging with practice assessments to gauge readiness for the certification exam [2]. |

**Resources:** Learners are encouraged to utilize the [Study guide for Exam AI-102](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-102) as a primary preparation tool [9].

---

## References

[1] [What is Microsoft Foundry? - Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)  
[2] [Training for Microsoft Foundry - Microsoft Learn](https://learn.microsoft.com/en-us/training/azure/ai-foundry)  
[3] [Retrieval augmented generation (RAG) and indexes - Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/concepts/retrieval-augmented-generation)  
[4] [Building Knowledge-Grounded AI Agents with Foundry IQ](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/building-knowledge-grounded-ai-agents-with-foundry-iq/4499683)  
[5] [Customize a model with fine-tuning - Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning)  
[6] [Microsoft Foundry documentation - Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/)  
[7] [Configure tracing for AI agent frameworks - Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/trace-agent-framework)  
[8] [Evaluating and Improving AI Agents at Scale with Microsoft Foundry](https://arize.com/blog/evaluating-and-improving-ai-agents-at-scale-with-microsoft-foundry/)  
[9] [Azure AI Engineer Associate - Certifications](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-engineer/)  
