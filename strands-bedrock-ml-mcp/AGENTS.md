# Agent Development Guidelines

This document provides a unified, research-backed reference for working with:

1. **Strands Agents SDK** (Python)
2. **LangGraph** (Python)
3. **OpenAI Agents SDK** (Python)
4. **AWS SageMaker**
5. **AWS Bedrock AgentCore** (Runtime / Gateway)

It integrates updated knowledge from official docs and external sources.

---

# 1. Principle: Always Retrieve Context First

Before acting, designing, or making suggestions:

* Use **context7** or **Perplexity MCP** to fetch relevant docs, API behaviors, known issues, and code references.
* Do not assume implementation details.
* Use retrieved context to guide code, architecture, and tool-schema decisions.

---

# 2. Framework at a Glance

### Strands Agents SDK

Lightweight, model-driven Python SDK for building agents quickly. Supports multi-provider models and MCP tool discovery.

### LangGraph

Graph-based orchestration for multi-agent workflows. Excellent for stateful systems, branching logic, loops, and persistent memory.

### OpenAI Agents SDK

Framework for structured agent behavior: tools, guardrails, sessions, handoffs. Strong observability and validation support.

### AWS SageMaker

Managed service for hosting, fine-tuning, and serving ML/LLM models. Often used as the model runtime for complex agent systems.

### AWS Bedrock AgentCore

Enterprise agent runtime and gateway. Provides execution environment, identity, memory, tool routing, and observability for production agents.

---

# 3. Unifying Mental Model

Across all frameworks, treat these as core concepts:

* **Agent**: LLM + instructions + state
* **Tools**: Functions/APIs the agent can call
* **Memory**: What persists across turns/sessions
* **Routing**: How control flow moves between tasks, tools, or agents
* **Execution Layer**: Where the agent runs (local, SageMaker, AgentCore)

---

# 4. Framework-Specific Notes

## Strands Agents SDK

* Uses function schemas for tools.
* Integrates with MCP servers for tool discovery.
* Good for rapid prototyping.
* Works well with multi-model environments (Bedrock, OpenAI, local models).

## LangGraph

* Build workflows as directed graphs.
* Nodes handle tool actions, retrieval, or sub-agent logic.
* Supports loops, branching, streaming, durable state.
* Ideal for multi-agent collaboration or tasks requiring deterministic flow.

## OpenAI Agents SDK

* Agents defined with instructions + tools.
* Handoffs allow delegation between multiple agents.
* Guardrails enforce schema validation.
* Sessions provide memory across interactions.
* Built-in observability and tracing.

## AWS SageMaker

* Used for training and hosting custom LLMs or fine-tuned variants.
* Choose instance type carefully based on latency/cost.
* Endpoint invocation must be integrated into the agent's toolchain.
* Secure using IAM roles.

## AWS Bedrock AgentCore

* Runtime executes agent logic in a secure, serverless environment.
* Gateway connects external tools and APIs.
* Supports long-running workflows (hours).
* Identity, memory, tokenization, and monitoring are built-in.
* Recommended for enterprise-grade deployment.

---

# 5. Validate Tools & I/O Contracts

Each framework defines tools differently:

* **Strands**: Python function schemas
* **LangGraph**: Node functions with explicit state
* **OpenAI Agents**: Tools via structured definitions
* **SageMaker**: Model endpoints treated as tools
* **AgentCore**: Tools exposed via Gateway with JSON schemas

Always verify:

* Input parameter names
* Return structure
* Error paths
* Streaming vs non-streaming behavior

---

# 6. Deployment Awareness

### If using SageMaker

* Real-time vs async endpoint
* Container image and inference handler
* IAM role configuration

### If using AgentCore

* Stateless execution requirement
* Gateway integration
* Tool definitions must use validated schemas
* Session identity and memory policies

### If using LangGraph

* Durable execution and checkpointing
* Graph complexity affects debug cost

### If using Strands or OpenAI SDKs

* Local dev is fine, but production may require SageMaker or AgentCore backends

---

# 7. Testing Strategy

Test at two levels:

### Functional Testing

* Tool correctness
* Schema validation
* Single-agent behavior

### Integration Testing

* Network + credentials
* Latency of SageMaker endpoints
* AgentCore runtime events
* Multi-agent handoff chains
* LangGraph routing and conditional branches

---

# 8. Error Handling & Observability

* Use structured logs
* Capture latencies for each tool call
* Validate chain-of-thought suppression / safe outputs
* Use AgentCore and OpenAI tracing when available
* Monitor model invocation cost

---

# 9. Security & Secrets

* Use environment variables or secret managers
* Avoid static credentials
* Prefer AWS IAM roles, SSO, or task roles
* Protect access to AgentCore and SageMaker endpoints

---

# 10. Maintenance

Update this doc when:

* Framework APIs change
* New deployment patterns emerge
* Additional runtimes or gateways are added

Focus on clarity and minimal duplication.
