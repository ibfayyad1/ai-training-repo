"""
Module 02 - Activity 1: Weak vs Strong Prompt
===============================================
Same AI, same report, same cost.
See how prompt quality changes everything.

Run: python activity-01-weak-vs-strong.py
Requires: OPENAI_API_KEY environment variable
"""

from openai import OpenAI
import json

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

REPORT = "Two trucks collided on the highway near exit 5. Fuel is leaking onto the road surface. One driver complaining of back pain. Traffic is blocked in both directions. Time approximately 14:30."

# --- WEAK PROMPT ---
weak_prompt = f"Classify this incident: {REPORT}"

# --- STRONG PROMPT ---
strong_prompt = f"""You are an incident classification specialist for a government reporting system.

Classify this report and extract key metadata.

Respond ONLY in this JSON format:
{{
  "category": "Traffic|Fire|Theft|Public Safety|Environmental",
  "severity": "low|medium|high|critical",
  "location": "extracted location",
  "timestamp": "extracted time or 'not mentioned'",
  "parties_involved": ["list of parties"],
  "summary": "1 sentence summary",
  "confidence": 0-100,
  "reasoning": "brief explanation of classification"
}}

Rules:
- If injuries mentioned → minimum severity = high
- If ongoing public danger → severity = critical
- Do NOT invent information not in the report
- No extra text. Only valid JSON.

Report: {REPORT}"""


def run_prompt(prompt, label):
    """Run a prompt and display the result."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


print("=" * 60)
print("WEAK vs STRONG PROMPT - Same report, same AI")
print("=" * 60)
print()
print(f"Report: {REPORT[:70]}...")
print()

# Run weak
print("--- WEAK PROMPT ---")
print('Prompt: "Classify this incident: [report]"')
print()
weak_result = run_prompt(weak_prompt, "Weak")
print(f"Result: {weak_result}")
print()

# Run strong
print("--- STRONG PROMPT ---")
print("Prompt: Role + Context + Task + Format + Constraints")
print()
strong_result = run_prompt(strong_prompt, "Strong")
print(f"Result:")
try:
    parsed = json.loads(strong_result)
    print(json.dumps(parsed, indent=2))
except json.JSONDecodeError:
    print(strong_result)

print()
print("=" * 60)
print("SAME AI. SAME COST. The only difference: how you asked.")
print("Strong prompt → structured data ready for your database.")
print("=" * 60)
print()
print("YOUR TURN: Change the REPORT variable at the top to your own")
print("incident and run again. See how both prompts handle it.")
