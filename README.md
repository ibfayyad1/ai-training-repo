# AI & LLM Training - Hands-On Activities

> 2-Day Training Program: From Fundamentals to Building a Full AI-Powered System

---

## What You Will Learn

| Day | Focus | What You Do |
|-----|-------|-------------|
| Day 1 | Theory + Hands-on Labs Experiments | Understand how AI works, practice with live code |
| Day 2 | Theory + Build a Full System | Build an AI-Powered Incident Report System (Flask + AI) |

---

## Training Modules

| # | Module | Key Concepts |
|---|--------|-------------|
| 01 | LLM Fundamentals | Tokens, Training Loop, Context Window, Temperature, Hallucination |
| 02 | Prompt Engineering | System Prompt, Few-Shot, Chain of Thought, JSON Output, Constraints |
| 03 | RAG & Knowledge Systems | Embeddings, Vector Search, Grounded Answers, Citations |
| 04 | AI Agents & Tools | ReAct Loop, Tool Use, Multi-Step, Safety |
| 05 | End-to-End Dev Lifecycle | 10 Stages from Requirements to Deployment with AI |
| -- | Capstone Project | Full Incident Report System (Backend + Frontend + AI) |

---

## Quick Start (PyCharm Terminal)

### Mac

```bash
cd ai-training-repo
pip3 install -r requirements.txt
echo 'OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE' > .env
cd module-01-llm-fundamentals
python3 activity-01-tokens.py
```

### Windows

```cmd
cd ai-training-repo
pip install -r requirements.txt
echo OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE > .env
cd module-01-llm-fundamentals
python activity-01-tokens.py
```

---

## Full Setup Guide

### Step 1: Install Python (if not installed)

| OS | How |
|----|-----|
| **Mac** | Already installed. Or run: `brew install python3` |
| **Windows** | Download from [python.org](https://www.python.org/downloads/) - check **"Add to PATH"** during install |

### Step 2: Clone this repo

```bash
git clone https://github.com/ibfayyad1/ai-training-repo.git
cd ai-training-repo
```

### Step 3: Install libraries

**Mac:**
```bash
pip3 install -r requirements.txt
```

**Windows:**
```cmd
pip install -r requirements.txt
```

### Step 4: Set your API key

Create a file called `.env` in the `ai-training-repo` folder:

```
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
```

Every script reads from this file automatically. Works with both terminal and PyCharm Run button.

### Step 5: Run an activity

**Mac:**
```bash
cd module-01-llm-fundamentals
python3 activity-01-tokens.py
```

**Windows:**
```cmd
cd module-01-llm-fundamentals
python activity-01-tokens.py
```

---

## Repo Structure

```
ai-training-repo/
|-- .env.example                       - API key template (copy to .env)
|-- requirements.txt                   - Python dependencies
|
|-- module-01-llm-fundamentals/        - Day 1: How AI works
|   |-- activity-01-tokens.py          - Token counting & cost (no API needed)
|   |-- activity-02-temperature.py     - Temperature effect on classification
|
|-- module-02-prompt-engineering/      - Day 1: How to talk to AI
|   |-- activity-01-weak-vs-strong.py  - Weak vs strong prompt comparison
|   |-- activity-02-few-shot.py        - Zero-shot vs few-shot accuracy
|   |-- activity-03-chain-of-thought.py - Step-by-step reasoning
|   |-- activity-04-build-system-prompt.py - Build your own system prompt
|
|-- module-03-rag/                     - Day 1: Connect AI to real data
|   |-- activity-01-embeddings.py      - Semantic similarity scores
|   |-- activity-02-mini-rag.py        - Build a RAG system (~80 lines)
|   |-- activity-03-rag-vs-no-rag.py   - Hallucination vs grounded answers
|
|-- module-04-agents/                  - Day 2: Give AI the ability to act
|   |-- activity-01-tool-use.py        - AI decides when to use tools
|   |-- activity-02-multi-step-agent.py - Agent: Classify -> Save -> Notify
|   |-- activity-03-build-your-tool.py - Define your own tool
|
|-- capstone-project/                  - Day 2: Build a full system
    |-- README.md                      - Capstone setup & docs
    |-- backend/                       - Flask API + AI services
    |   |-- run.py                     - Start server (python run.py)
    |   |-- requirements.txt           - Backend dependencies
    |   |-- app/
    |       |-- models/                - Database (SQLite)
    |       |-- services/              - AI, RAG, Agent, PDF
    |       |-- controllers/           - API endpoints
    |       |-- templates/             - Frontend UI (HTML/JS)
    |-- frontend/                      - Angular source (optional)
```

---

## How to Use

1. Open the activity file in your editor
2. Read the comments at the top - they explain what's happening
3. Run it in the terminal
4. **Try your own inputs** - each file has a "YOUR TURN" section

---

## Capstone Project (Day 2)

A full AI-Powered Incident Report System with:
- AI Agent that classifies, analyzes images, saves, generates reports, and notifies teams
- RAG-powered Q&A chat (ask questions about your incidents)
- PDF report generation
- Dashboard with statistics

See [capstone-project/README.md](capstone-project/README.md) for full docs.

**Quick run:**
```bash
cd capstone-project/backend
pip install -r requirements.txt
echo 'OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE' > .env
python run.py
# Open: http://localhost:5001
```
