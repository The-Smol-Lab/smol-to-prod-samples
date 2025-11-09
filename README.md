# Smol-to-Production Series

**Learn how to turn small AI ideas into real, usable apps.**
This repo is your hands-on guide to building, testing, and deploying AI systems — step by step.

## Overview

Each folder teaches one clear stage of the journey, from brainstorming to production. You can follow along, skip ahead, or remix the steps for your own project.

### 🧭 Learning Path

| Step                  | Focus                                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------------- |
| 1️⃣ Requirements      | What problem are you solving? What data or APIs do you need?                                       |
| 2️⃣ Design            | Sketch the workflow, roles, and data flow. Decide what AI should (and shouldn’t) do.               |
| 3️⃣ Build             | Write the core app or model logic. Keep it modular and simple.                                     |
| 4️⃣ Test              | Run locally, catch errors early, and ensure reproducibility.                                       |
| 5️⃣ Evaluate          | Check accuracy, latency, and cost — adjust until it feels right.                                   |
| 6️⃣ Frontend          | Add a UI (choose Streamlit for quick demos, Open WebUI for chat-style, or Next.js for production). |
| 7️⃣ Deploy            | Push to Railway, Render, or AWS when you’re ready to share it.                                     |
| 8️⃣ Monitor & Improve | Track logs, usage, and iterate over time.                                                          |

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
