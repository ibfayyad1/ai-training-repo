# Module 04 - AI Agents & Tools

## Activities

| # | File | What You Learn |
|---|------|---------------|
| 1 | `activity-01-tool-use.py` | AI decides when to use tools vs answer directly |
| 2 | `activity-02-multi-step-agent.py` | Agent performs: Classify → Save → Notify |
| 3 | `activity-03-build-your-tool.py` | Define your own tool and test it |

## Run

```bash
export OPENAI_API_KEY="your-key"

python activity-01-tool-use.py       # Simple tool use
python activity-02-multi-step-agent.py  # Multi-step agent
python activity-03-build-your-tool.py   # Build your own
```

## Key Concepts

- **Chatbot vs Agent**: Chatbot only talks. Agent takes actions.
- **Tool Use**: Give AI functions it can call (search, save, notify)
- **ReAct Loop**: Thought → Action → Observation → Repeat
- **Function Calling**: How to define tools in code (OpenAI format)
- **Safety**: Read tools = free. Write tools = need confirmation.
