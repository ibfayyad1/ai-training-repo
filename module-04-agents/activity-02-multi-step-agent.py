"""
Module 04 - Activity 2: Multi-Step Agent
==========================================
An agent that performs multiple actions:
Search → Classify → Save → Notify

See the full ReAct loop (Thought → Action → Observation).

Run: python activity-02-multi-step-agent.py
Requires: OPENAI_API_KEY environment variable
"""

from openai import OpenAI
import json
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# ============================================================
# Simulated system (database + notification)
# ============================================================

saved_reports = []
sent_notifications = []


def classify_incident(report_text: str) -> str:
    """Tool: Classify an incident report."""
    # Simple keyword-based classification (in real system, this would be AI-powered)
    text = report_text.lower()
    if any(w in text for w in ["collision", "crash", "traffic", "vehicle", "car", "truck"]):
        category = "Traffic"
    elif any(w in text for w in ["fire", "smoke", "flames", "burning"]):
        category = "Fire"
    elif any(w in text for w in ["stolen", "theft", "robbery", "break-in"]):
        category = "Theft"
    else:
        category = "Public Safety"

    severity = "critical" if any(w in text for w in ["serious", "critical", "fatal"]) else \
               "high" if any(w in text for w in ["injur", "hurt", "ambulance"]) else "medium"

    return json.dumps({"category": category, "severity": severity})


def save_report(category: str, severity: str, summary: str, location: str) -> str:
    """Tool: Save incident report to database."""
    report_id = f"IR-{len(saved_reports) + 5001}"
    report = {
        "id": report_id,
        "category": category,
        "severity": severity,
        "summary": summary,
        "location": location,
        "timestamp": datetime.now().isoformat(),
        "status": "open"
    }
    saved_reports.append(report)
    return json.dumps({"success": True, "report_id": report_id, "message": f"Report {report_id} saved successfully"})


def send_alert(team: str, message: str, priority: str = "normal") -> str:
    """Tool: Send alert to response team."""
    alert = {"team": team, "message": message, "priority": priority, "time": datetime.now().isoformat()}
    sent_notifications.append(alert)
    return json.dumps({"success": True, "message": f"Alert sent to {team} team with {priority} priority"})


# Tool definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "classify_incident",
            "description": "Classify an incident report text into category and severity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "report_text": {"type": "string", "description": "The incident report text to classify"}
                },
                "required": ["report_text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_report",
            "description": "Save a classified incident report to the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Incident category"},
                    "severity": {"type": "string", "description": "Severity level"},
                    "summary": {"type": "string", "description": "Brief summary"},
                    "location": {"type": "string", "description": "Location of incident"}
                },
                "required": ["category", "severity", "summary", "location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_alert",
            "description": "Send an alert notification to a response team.",
            "parameters": {
                "type": "object",
                "properties": {
                    "team": {"type": "string", "description": "Team to notify (traffic, fire, theft, general)"},
                    "message": {"type": "string", "description": "Alert message"},
                    "priority": {"type": "string", "enum": ["low", "normal", "high", "urgent"], "description": "Alert priority"}
                },
                "required": ["team", "message"]
            }
        }
    }
]

# Available functions
AVAILABLE_FUNCTIONS = {
    "classify_incident": classify_incident,
    "save_report": save_report,
    "send_alert": send_alert,
}


# ============================================================
# Multi-step agent loop
# ============================================================

def run_multi_step_agent(user_input, max_steps=5):
    """Run agent that can take multiple actions."""

    print(f"\nUser: {user_input}")
    print("=" * 50)

    messages = [
        {"role": "system", "content": """You are an incident management agent. When a user reports an incident:
1. First classify it (use classify_incident tool)
2. Then save it to the database (use save_report tool)
3. Then send an alert to the appropriate team (use send_alert tool)

Always complete all 3 steps. Think step by step."""},
        {"role": "user", "content": user_input}
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        msg = response.choices[0].message

        # If no tool calls, we're done
        if not msg.tool_calls:
            print(f"\n  Final Answer: {msg.content}")
            break

        # Process each tool call
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            print(f"\n  Step {step + 1} - Action: {func_name}")
            print(f"    Args: {json.dumps(func_args, indent=2)[:200]}")

            # Execute
            func = AVAILABLE_FUNCTIONS[func_name]
            result = func(**func_args)

            print(f"    Result: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    print("=" * 50)


# ============================================================
# Test
# ============================================================

print("=" * 60)
print("MULTI-STEP AGENT - Classify → Save → Notify")
print("=" * 60)

# Test case 1
run_multi_step_agent(
    "Report an incident: Two vehicles collided on Highway 7 near exit 3. "
    "One driver has serious neck injuries. Ambulance needed. Road partially blocked."
)

print()

# Test case 2
run_multi_step_agent(
    "There's smoke coming from the warehouse in Industrial Zone B. "
    "Flames visible from the roof. No injuries reported yet."
)

# Summary
print("\n")
print("=" * 60)
print("AGENT SUMMARY")
print("=" * 60)
print(f"\n  Reports saved: {len(saved_reports)}")
for r in saved_reports:
    print(f"    {r['id']}: {r['category']} ({r['severity']}) - {r['summary'][:50]}")

print(f"\n  Alerts sent: {len(sent_notifications)}")
for n in sent_notifications:
    print(f"    → {n['team']} team ({n['priority']}): {n['message'][:50]}")

print("\n")
print("KEY INSIGHT: The agent completed 3 actions per report -")
print("classify, save, notify - all automatically from natural language input.")
print("=" * 60)
print()
print("YOUR TURN: Write your own incident report and pass it to run_multi_step_agent().")
print("Example: run_multi_step_agent('Laptop stolen from office in Building C, 3rd floor')")
