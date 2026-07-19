"""
Module 04 - Activity 3: Build Your Own Tool
=============================================
Challenge: Define a new tool and give it to the AI.
See if the AI uses it correctly.

Run: python activity-03-build-your-tool.py
Requires: OPENAI_API_KEY environment variable
"""

from openai import OpenAI
import json

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# ============================================================
# YOUR CHALLENGE: Define a new tool
# ============================================================

# Example: A tool that gets statistics for an area
def get_area_statistics(area: str, period: str = "this_month") -> str:
    """
    YOUR TOOL: Returns incident statistics for a given area.
    In production, this would query your real database.
    """
    # Simulated data
    fake_stats = {
        "eastern": {"total": 45, "traffic": 28, "fire": 7, "theft": 10, "period": period},
        "western": {"total": 32, "traffic": 18, "fire": 5, "theft": 9, "period": period},
        "central": {"total": 67, "traffic": 41, "fire": 12, "theft": 14, "period": period},
    }

    area_lower = area.lower()
    if area_lower in fake_stats:
        return json.dumps(fake_stats[area_lower])
    else:
        return json.dumps({"error": f"No data found for area: {area}"})


# TODO: Try adding your own tool! Examples:
# - get_weather(location) → returns weather data
# - assign_officer(incident_id, officer_name) → assigns an officer
# - close_incident(incident_id, resolution) → closes a case


# ============================================================
# Tool definition (this is what you send to the AI)
# ============================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_area_statistics",
            "description": "Get incident statistics for a specific area. Returns total incidents broken down by type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "area": {
                        "type": "string",
                        "description": "Area name (e.g., 'Eastern', 'Western', 'Central')"
                    },
                    "period": {
                        "type": "string",
                        "description": "Time period (e.g., 'this_month', 'this_week', 'today')"
                    }
                },
                "required": ["area"]
            }
        }
    }
]

AVAILABLE_FUNCTIONS = {
    "get_area_statistics": get_area_statistics,
}


# ============================================================
# Agent loop
# ============================================================

def ask_agent(question):
    """Run agent with your custom tool."""
    print(f"\nQ: {question}")
    print("-" * 40)

    messages = [
        {"role": "system", "content": "You are an incident statistics assistant. Use available tools to get real data. Never invent numbers."},
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages,
        tools=TOOLS, temperature=0
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            print(f"  Tool used: {func_name}({func_args})")

            result = AVAILABLE_FUNCTIONS[func_name](**func_args)
            print(f"  Result: {result}")

            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

        final = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, temperature=0
        )
        print(f"  Answer: {final.choices[0].message.content}")
    else:
        print(f"  Answer: {msg.content}")


# ============================================================
# Test
# ============================================================

print("=" * 60)
print("YOUR CUSTOM TOOL IN ACTION")
print("=" * 60)

ask_agent("How many incidents were reported in the Eastern area this month?")
ask_agent("Compare traffic incidents between Eastern and Western areas.")
ask_agent("Which area has the most incidents?")
ask_agent("Hi, what can you help me with?")  # Should NOT use tool

print()
print("=" * 60)
print("YOUR TURN:")
print("  1. Modify get_area_statistics to add more areas")
print("  2. Add a new tool (e.g., get_weather, assign_officer)")
print("  3. Add it to TOOLS and AVAILABLE_FUNCTIONS")
print("  4. Ask questions that should trigger your new tool")
print("=" * 60)
