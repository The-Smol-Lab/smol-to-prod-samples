# Smol-to-Production Series

**Learn how to turn small AI ideas into real, usable apps.**
This repo is your hands-on guide to building, testing, and deploying AI systems — step by step.

## Overview

Each folder teaches one clear stage of the journey, from brainstorming to production. You can follow along, skip ahead, or remix the steps for your own project.

### 🧭 Learning Path

### 🧭 Learning Path

| Step | Focus |
|------|--------|
| **1️⃣ Requirements** | Start by defining the problem and who it helps. Clarify your goals, success metrics, and the data or APIs your app will rely on. |
| **2️⃣ Design** | Outline the workflow and system roles. Separate what should be handled by AI versus traditional logic. Select your **agentic framework** (LangGraph, OpenAI Agent SDK, Strands Agents, etc.) and **base model** (GPT, Claude, Gemini, etc.). Decide whether to use **custom tools** or **MCP (Model Context Protocol)** for integration. Run small-scale prompt or data tests to confirm feasibility before coding. |
| **3️⃣ Build** | Implement the core logic and AI pipeline. Keep your modules clean, reusable, and easy to iterate on. |
| **4️⃣ Test** | Verify functionality in a local environment. Catch bugs early, confirm reproducibility, and make sure every dependency works as expected. |
| **5️⃣ Evaluate** | Measure performance across accuracy, latency, and cost. Fine-tune prompts, parameters, or data pipelines until results feel consistent. |
| **6️⃣ Frontend** | Build a usable interface — **Streamlit** for quick demos, **Open WebUI** for chat-style apps, or **Next.js** for production-grade deployment. |
| **7️⃣ Deploy** | Launch to the cloud using **Railway**, **Render**, or **AWS (ECS/Fargate + S3)**. Automate builds and environment configs when possible. |
| **8️⃣ Monitor & Improve** | Track logs, usage, and performance metrics. Gather feedback and iterate on both backend logic and user experience over time. |



## 🚀 Quickstart

```bash
git clone https://github.com/The-Smol-Lab/smol-to-prod-samples.git
cd smol-to-prod-samples
cp .env.example .env
docker compose up --build
```

Visit: [http://localhost:3000](http://localhost:3000)

## 🧩 Choose Your Stack

| Goal               | Recommended Tool  |
| ------------------ | ----------------- |
| Fast prototype     | Streamlit         |
| Conversational UI  | Open WebUI        |
| Production web app | Next.js + FastAPI |

## ☁️ Deployment Options

* **One-click preview:** [Railway](https://railway.app/new) • [Render](https://render.com/deploy)
* **Production scale:** AWS (ECS/Fargate + CloudFront + S3)

## 📁 Folder Layout

```
smol-to-prod-samples/
├── lessons/   # step-by-step learning modules
├── examples/  # runnable demos
├── docs/      # deeper guides
├── assets/    # diagrams, screenshots
└── .env.example
```

## 💡 Next Steps

* Try the `examples/minimal-demo` to get started fast.
* Explore `lessons/` for deeper learning.
* Deploy your version to the cloud and monitor it.

---

**License:** Apache 2.0
