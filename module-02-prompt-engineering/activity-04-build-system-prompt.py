"""
Module 02 - Activity 4: Build Your System Prompt
==================================================
Challenge: Build a complete system prompt for 
an incident classification system.

This file has the TEMPLATE - you fill in the blanks.
Then run it to test with sample reports.

Run: python activity-04-build-system-prompt.py
Requires: OPENAI_API_KEY environment variable
"""

from openai import OpenAI
import json

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# ============================================================
# YOUR CHALLENGE: Complete this system prompt
# Fill in the sections marked with [TODO]
# ============================================================

SYSTEM_PROMPT = """
You are [TODO: define the AI's role].

CATEGORIES:
[TODO: list your incident categories]

SEVERITY SCALE:
[TODO: define severity levels and when to use each]

OUTPUT FORMAT:
Respond ONLY in this JSON format:
{
  "category": "",
  "severity": "",
  "location": "",
  "timestamp": "",
  "summary": "",
  "confidence": 0-100
}

CONSTRAINTS:
[TODO: list at least 3 rules the AI must follow]
"""

# ============================================================
# EXAMPLE SOLUTION (uncomment to use)
# ============================================================

EXAMPLE_SOLUTION = """
You are the classification engine for a government incident reporting system.
You process incoming incident reports and extract structured data.

CATEGORIES (pick exactly ONE):
- Traffic: vehicle collisions, road blockages, pedestrian incidents
- Fire: flames, smoke, explosions, burning
- Theft: stolen property, break-ins, robbery
- Public Safety: suspicious activity, infrastructure damage, public hazards
- Environmental: spills, pollution, waste, contamination

SEVERITY SCALE:
- low: no injuries, no ongoing danger, minor inconvenience
- medium: minor injuries OR moderate property damage
- high: serious injuries OR significant public disruption
- critical: life-threatening OR ongoing danger to public

OUTPUT FORMAT:
Respond ONLY in valid JSON:
{
  "category": "Traffic|Fire|Theft|Public Safety|Environmental",
  "severity": "low|medium|high|critical",
  "location": "extracted location or 'not mentioned'",
  "timestamp": "extracted time or 'not mentioned'",
  "summary": "1 sentence summary",
  "confidence": 0-100
}

CONSTRAINTS:
- Do NOT invent information not present in the report
- Do NOT classify as 'Other' - always pick the closest category
- Do NOT provide legal opinions or recommendations
- If injuries are mentioned → minimum severity = high
- If weapons/explosives mentioned → severity = critical
- If confidence < 70 → add "needs_review": true
- Respond in the same language as the input report
- No extra text outside JSON
"""

# ============================================================
# TEST YOUR PROMPT
# ============================================================

# Use example solution (replace with YOUR prompt when ready)
active_prompt = EXAMPLE_SOLUTION

TEST_REPORTS = [
    "Car hit a pedestrian near the mall. Ambulance called. Victim conscious but unable to walk.",
    "Strong smell of gas reported in residential building, 3rd floor. Residents evacuating.",
    "Broken glass and items scattered on floor of electronics shop. Owner says nothing was open overnight.",
    "Large pothole opened on main road after heavy rain. Multiple cars swerving to avoid it.",
    "Oil leaking from parked tanker truck into storm drain near the park.",
]

print("=" * 60)
print("TESTING YOUR SYSTEM PROMPT")
print("=" * 60)
print()

for i, report in enumerate(TEST_REPORTS, 1):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": active_prompt},
            {"role": "user", "content": f"Classify this report: {report}"}
        ]
    )

    result = response.choices[0].message.content.strip()
    print(f"Report {i}: {report[:60]}...")

    try:
        parsed = json.loads(result)
        print(f"  → {parsed['category']} | {parsed['severity']} | confidence: {parsed['confidence']}")
    except (json.JSONDecodeError, KeyError):
        print(f"  → {result[:80]}")
    print()

print("=" * 60)
print("YOUR TURN: Replace EXAMPLE_SOLUTION with your own prompt!")
print("Then run again and compare results.")
print("=" * 60)
