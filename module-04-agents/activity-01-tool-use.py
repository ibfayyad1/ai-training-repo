"""
Module 04 - Activity 1: Simple Tool Use
=========================================
Give AI a tool. Watch it decide when to use it.
The AI searches a database instead of guessing.

Run: python activity-01-tool-use.py
Requires: OPENAI_API_KEY environment variable
"""

from openai import OpenAI
import json

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# ============================================================
# STEP 1: Define our "database" (simulated)
# ============================================================

INCIDENT_DATABASE = [
    {"id": "IR-001", "type": "Traffic", "location": "Highway 7", "date": "2024-07-14", "severity": "high", "summary": "Two cars collided, one injury"},
    {"id": "IR-002", "type": "Fire", "location": "Zone B warehouse", "date": "2024-07-13", "severity": "high", "summary": "Warehouse fire, no injuries"},
    {"id": "IR-003", "type": "Theft", "location": "City Mall", "date": "2024-07-12", "severity": "medium", "summary": "Motorcycle stolen from parking"},
    {"id": "IR-004", "type": "Traffic", "location": "Main Street", "date": "2024-07-14", "severity": "critical", "summary": "Truck hit pedestrian, serious injuries"},
    {"id": "IR-005", "type": "Traffic", "location": "Expressway", "date": "2024-07-15", "severity": "high", "summary": "5-car pile-up in fog, 3 minor injuries"},
    {"id": "IR-006", "type": "Environmental", "location": "Ring Road", "date": "2024-07-13", "severity": "medium", "summary": "Oil spill from delivery truck"},
]


# ============================================================
# STEP 2: Define the tool (function the AI can call)
# ============================================================

def search_incidents(query: str, incident_type: str = None) -> str:
    """Search incidents - our 'tool' that AI can call."""
    results = INCIDENT_DATABASE

    if incident_type:
        results = [r for r in results if r["type"].lower() == incident_type.lower()]

    # Simple keyword search
    if query:
        query_lower = query.lower()
        results = [r for r in results if
                   query_lower in r["summary"].lower() or
                   query_lower in r["location"].lower() or
                   query_lower in r["type"].lower()]

    if not results:
        # If keyword search fails, return all (simulating semantic search)
        results = INCIDENT_DATABASE[:3] if not incident_type else []

    return json.dumps(results[:5], indent=2)


# Tool definition for OpenAI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_incidents",
            "description": "Search the incident report database. Use this whenever the user asks about incidents, statistics, or reports.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'highway', 'fire', 'injuries')"
                    },
                    "incident_type": {
                        "type": "string",
                        "enum": ["Traffic", "Fire", "Theft", "Public Safety", "Environmental"],
                        "description": "Filter by incident type (optional)"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


# ============================================================
# STEP 3: Run the agent loop
# ============================================================

def run_agent(user_question):
    """Run agent with tool use."""
    print(f"\nUser: {user_question}")
    print("-" * 50)

    messages = [
        {"role": "system", "content": "You are an incident report assistant. Use the search_incidents tool to find real data before answering. Never invent statistics."},
        {"role": "user", "content": user_question}
    ]

    # First call - AI decides whether to use tool
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
        temperature=0
    )

    msg = response.choices[0].message

    # Check if AI wants to use a tool
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            print(f"  AI Decision: Use tool '{func_name}'")
            print(f"  Arguments: {func_args}")

            # Execute the tool
            result = search_incidents(**func_args)
            print(f"  Tool Result: {result[:100]}...")

            # Send result back to AI
            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        # Get final answer
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0
        )
        print(f"\n  AI Answer: {final_response.choices[0].message.content}")
    else:
        print(f"  AI Answer (no tool needed): {msg.content}")


# ============================================================
# STEP 4: Test with different questions
# ============================================================

print("=" * 60)
print("AI AGENT WITH TOOL USE")
print("=" * 60)

QUESTIONS = [
    "What traffic accidents happened recently?",
    "Were there any fires this week?",
    "What's the most serious incident on record?",
    "Hello, how are you?",  # Should NOT use tool for this!
]

for q in QUESTIONS:
    run_agent(q)
    print()

print("=" * 60)
print("KEY OBSERVATIONS:")
print("  1. AI DECIDES when to use the tool (not every time)")
print("  2. It searches REAL data instead of inventing answers")
print("  3. Simple greetings don't trigger a search")
print("  4. It formats the tool results into natural language")
print("=" * 60)
print()
print("YOUR TURN: Add your own questions to the QUESTIONS list and run again.")
print("Try: 'What happened on the expressway?' or 'Any environmental issues?'")
