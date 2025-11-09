# Smol-to-Production Series

Practical experiments on scaling small AI projects into production-ready systems.

---

## Core Design Decisions
1. **Folder Structure** – one agent per folder vs shared utilities  
2. **Evaluation** – dataset design, metrics, reproducibility  
3. **Prompt Engineering** – versioning, testing, refinement loops  
4. **Workflow Automation** – human-in-the-loop pipelines  
5. **Database, Chunking & Caching** – how often to chunk, store, and reuse embeddings  
6. **Platform Choice** – Railway vs Render vs AWS (trade-offs)

---

## Local Development
1. `.env` configuration (API keys, base URLs, secrets)  
2. Agentic Framework – LangGraph, OpenAI-Agent-SDK, or Strands-Agents  
3. Model Backend – GPT, Gemini, Claude, Qwen, DeepSeek, etc.  
4. Tool Integration – Local vs MCP (why custom tools win)  
5. Prompts – modular, reusable, and versioned  
6. Memory – short-term & long-term strategies  
7. Knowledge Base – local or remote document storage  
8. **Caching** – response cache, retrieval cache, and embedding reuse for cost reduction

---

## Testing
- Run locally as Docker container  
- Load-test for concurrent requests  
- Validate caching efficiency and memory persistence

---

## Deployment
1. FastAPI backend  
2. Containerization (Docker)  
3. Cloud Hosting – Provisioned VM vs Serverless (Lambda/Fargate/AgentCore)  
4. Distributed caching layer (Redis, DynamoDB TTL, or in-memory)

---

## Authentication
- Inbound & outbound auth strategies (API tokens, OAuth, service accounts)

---

## Monitoring & Observability
- Langfuse for traces  
- AgentCore observability  
- LiteLLM request metrics  
- Cache hit/miss tracking

---

## Local vs Cloud Differences
- Cost, latency, scaling, caching behavior, and state persistence

---

**Source:** [The-Smol-Lab/smol-to-prod-samples (dev branch)](https://github.com/The-Smol-Lab/smol-to-prod-samples/tree/dev)
