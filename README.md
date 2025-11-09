# Smol-to-Production Series

**Learn how to turn small AI ideas into real, usable apps.**
This repo is your hands-on guide to building, testing, and deploying AI systems — step by step.

## Overview

Each folder teaches one clear stage of the journey, from brainstorming to production. You can follow along, skip ahead, or remix the steps for your own project.

### 🧭 Learning Path

| Step | Focus |
|------|--------|
| **1️⃣ Requirements** | Define the problem clearly. Identify who benefits, what success looks like, and what data or APIs you’ll need to solve it. |
| **2️⃣ Design** | Map the workflow, data flow, and system roles. Decide which parts need AI vs. traditional logic. Choose your agentic framework (LangGraph, OpenAI Agent SDK, Strands Agents, etc.) and initial model (GPT, Claude, Gemini, etc.). Decide whether to build **custom tools** or use **MCP (Model Context Protocol)** for integration. Run quick prompt or data tests to validate feasibility before building. |
| **3️⃣ Build** | Implement the core logic or model pipeline. Keep components modular and readable for easy iteration. |
| **4️⃣ Test** | Validate locally. Catch errors early, ensure reproducibility, and confirm all dependencies work as expected. |
| **5️⃣ Evaluate** | Measure accuracy, latency, and cost trade-offs. Tune prompts, parameters, or data until results feel reliable. |
| **6️⃣ Frontend** | Add a user interface — use **Streamlit** for quick prototypes, **Open WebUI** for chat workflows, or **Next.js** for full production apps. |
| **7️⃣ Deploy** | Launch your app to the cloud using **Railway**, **Render**, or **AWS (ECS/Fargate + S3)** once it’s stable. |
| **8️⃣ Monitor & Improve** | Track logs, performance, and usage. Collect feedback and keep refining both UX and backend logic over time. |


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
