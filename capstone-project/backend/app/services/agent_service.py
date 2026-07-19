"""
Agent Service - AI Agent with Tools (Module 04)
=================================================
This is the AGENTIC AI component of our system.
The agent receives a report and DECIDES what actions to take.

MODULE 04 CONCEPTS DEMONSTRATED:
┌──────────────────────────────────────────────────────────────────┐
│ • ReAct Pattern: Thought → Action → Observation → Repeat         │
│ • Tool Use: Agent has functions it can call (classify, analyze,  │
│   save, generate PDF, notify)                                     │
│ • Multi-Step: Agent performs 3-5 steps automatically             │
│ • Decision Making: Agent decides WHICH tools based on context    │
│   (e.g., skip image analysis if no image provided)               │
│ • Safety: Max iterations prevent infinite loops                  │
└──────────────────────────────────────────────────────────────────┘

DIFFERENCE FROM AI SERVICE:
- ai_service.py = individual AI functions (one task each)
- agent_service.py = orchestrator that DECIDES which functions to call and in what order
"""

import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


# ============================================================
# TOOL DEFINITIONS (what the agent can do)
# These are the "tools" we give to the AI agent.
# The agent DECIDES which to use based on the situation.
# ============================================================

AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "classify_incident",
            "description": "Classify an incident report into category (Traffic/Fire/Theft/Public Safety/Environmental) and severity (low/medium/high/critical). Use this first for any new incident.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "The incident report text to classify"
                    }
                },
                "required": ["description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_image",
            "description": "Analyze an incident scene image to describe what happened. Only use this if an image was provided with the report.",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the uploaded image file"
                    }
                },
                "required": ["image_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_incident",
            "description": "Save the classified incident to the database. Use after classification is complete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Original report text"},
                    "category": {"type": "string", "description": "Classified category"},
                    "severity": {"type": "string", "description": "Severity level"},
                    "location": {"type": "string", "description": "Extracted location"},
                    "timestamp_extracted": {"type": "string", "description": "Extracted time"},
                    "image_analysis": {"type": "string", "description": "Image analysis result or null"},
                    "reporter_username": {"type": "string", "description": "Username of reporter"}
                },
                "required": ["description", "category", "severity", "reporter_username"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_report",
            "description": "Generate a professional PDF-ready incident report. Use after classification and (optional) image analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "incident_id": {
                        "type": "integer",
                        "description": "The ID of the saved incident"
                    }
                },
                "required": ["incident_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_notification",
            "description": "Send a notification to the appropriate response team. Use for high or critical severity incidents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "team": {
                        "type": "string",
                        "enum": ["traffic", "fire", "theft", "public_safety", "environmental"],
                        "description": "Team to notify based on category"
                    },
                    "severity": {
                        "type": "string",
                        "description": "Severity level of the incident"
                    },
                    "message": {
                        "type": "string",
                        "description": "Notification message"
                    }
                },
                "required": ["team", "severity", "message"]
            }
        }
    }
]


# ============================================================
# TOOL IMPLEMENTATIONS (actual functions the agent calls)
# ============================================================

def _tool_classify(description: str) -> str:
    """Execute classification tool."""
    from app.services.ai_service import classify_incident
    result = classify_incident(description)
    return json.dumps(result)


def _tool_analyze_image(image_path: str) -> str:
    """Execute image analysis tool."""
    from app.services.ai_service import analyze_image
    result = analyze_image(image_path)
    return json.dumps({"analysis": result})


def _tool_save_incident(description: str, category: str, severity: str,
                        reporter_username: str, location: str = "not specified",
                        timestamp_extracted: str = "not specified",
                        image_analysis: str = None) -> str:
    """Execute save to database tool."""
    from app.models.database import create_incident
    data = {
        "description": description,
        "category": category,
        "severity": severity,
        "location": location,
        "timestamp_extracted": timestamp_extracted,
        "image_analysis": image_analysis,
        "reporter_username": reporter_username
    }
    result = create_incident(data)
    return json.dumps(result)


def _tool_generate_report(incident_id: int) -> str:
    """Execute report generation tool."""
    from app.models.database import get_incident_by_id
    from app.services.ai_service import generate_report

    incident = get_incident_by_id(incident_id)
    if not incident:
        return json.dumps({"error": "Incident not found"})

    classification = {
        "category": incident["category"],
        "severity": incident["severity"],
        "location": incident["location"],
        "timestamp_extracted": incident["timestamp_extracted"],
        "confidence": incident["confidence"],
        "reasoning": incident["ai_reasoning"]
    }

    report = generate_report(
        incident["description"],
        classification,
        incident.get("image_analysis")
    )
    return json.dumps({"report": report, "incident_id": incident_id})


def _tool_send_notification(team: str, severity: str, message: str) -> str:
    """Execute notification tool (simulated - in production this would send real alerts)."""
    # In production: send email, SMS, push notification
    # For training: we simulate it
    notification = {
        "sent": True,
        "team": team,
        "severity": severity,
        "message": message,
        "note": "Notification simulated for training"
    }
    return json.dumps(notification)


# Map tool names to implementations
TOOL_FUNCTIONS = {
    "classify_incident": _tool_classify,
    "analyze_image": _tool_analyze_image,
    "save_incident": _tool_save_incident,
    "generate_report": _tool_generate_report,
    "send_notification": _tool_send_notification,
}


# ============================================================
# THE AGENT - ReAct Loop (Module 04 Core Concept)
# ============================================================

def process_incident_with_agent(description: str, image_path: str = None,
                                reporter_username: str = "reporter1") -> dict:
    """
    Process an incident using the AI Agent.

    THE REACT LOOP:
    ┌────────────────────────────────────────────────────────────┐
    │  1. Agent receives the report                              │
    │  2. Agent THINKS: "What should I do first?"               │
    │  3. Agent ACTS: Calls a tool (e.g., classify)             │
    │  4. Agent OBSERVES: Gets the result                       │
    │  5. Agent THINKS: "What next?" → Repeats until done       │
    │                                                            │
    │  The agent decides the workflow based on context:           │
    │  - Has image? → analyze it                                │
    │  - High severity? → send notification                     │
    │  - Always: classify → save → generate report              │
    └────────────────────────────────────────────────────────────┘

    MAX ITERATIONS: 8 (safety limit - prevents infinite loops)
    """

    # Build initial context for the agent
    user_message = f"""Process this new incident report:

DESCRIPTION: {description}
REPORTER: {reporter_username}
IMAGE PROVIDED: {"Yes - path: " + image_path if image_path else "No"}

Instructions:
1. First, classify the incident (category + severity)
2. If an image is provided, analyze it
3. Save the incident to the database
4. Generate a professional report
5. If severity is high or critical, send a notification to the appropriate team

Complete all necessary steps."""

    # ---- SYSTEM PROMPT (Module 02: Role for the Agent) ----
    system_prompt = """You are an intelligent incident processing agent.
You have access to tools that let you classify, analyze, save, report, and notify.
Think step by step about what actions are needed, then execute them in order.
Always complete the full workflow: classify → (analyze image if present) → save → generate report → (notify if severe).
After all actions are complete, provide a final summary to the user."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    # ---- THE REACT LOOP (Module 04) ----
    max_iterations = 8   # Safety: prevent infinite loops
    actions_taken = []    # Log all actions for audit trail

    for iteration in range(max_iterations):
        # Agent decides what to do
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,           # Deterministic decisions
            messages=messages,
            tools=AGENT_TOOLS
        )

        message = response.choices[0].message

        # If no tool calls → agent is done, return final answer
        if not message.tool_calls:
            return {
                "success": True,
                "final_answer": message.content,
                "actions_taken": actions_taken,
                "iterations": iteration + 1
            }

        # Process each tool call
        messages.append(message)

        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            # Log the action (for audit trail)
            actions_taken.append({
                "step": len(actions_taken) + 1,
                "tool": func_name,
                "arguments": func_args
            })

            # Execute the tool
            if func_name in TOOL_FUNCTIONS:
                result = TOOL_FUNCTIONS[func_name](**func_args)
            else:
                result = json.dumps({"error": f"Unknown tool: {func_name}"})

            # Add result back to messages (agent sees the observation)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    # If we hit max iterations - safety stop
    return {
        "success": False,
        "final_answer": "Agent reached maximum iterations. Partial processing completed.",
        "actions_taken": actions_taken,
        "iterations": max_iterations
    }
