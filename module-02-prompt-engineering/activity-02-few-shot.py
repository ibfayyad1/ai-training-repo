"""
Module 02 - Activity 2: Zero-Shot vs Few-Shot
===============================================
See how 3 examples dramatically improve accuracy.
No training. No fine-tuning. Just examples in the prompt.

Run: python activity-02-few-shot.py
Requires: OPENAI_API_KEY environment variable
"""

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# An ambiguous report that could go multiple ways
AMBIGUOUS_REPORT = "Person reported seeing smoke near an electrical transformer at night, strong burning smell in the area"


def classify_zero_shot(report):
    """Classify with no examples."""
    prompt = f"""Classify this incident into ONE category:
- Traffic
- Fire  
- Theft
- Public Safety
- Environmental

Report: "{report}"

Respond with: category | confidence (0-100)"""

    response = client.chat.completions.create(
        model="gpt-4o-mini", temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def classify_few_shot(report):
    """Classify with 3 examples showing the pattern."""
    prompt = f"""Classify this incident into ONE category:
- Traffic
- Fire  
- Theft
- Public Safety
- Environmental

Examples:
Report: "Car hit a pedestrian near the mall at 3pm, ambulance called"
→ Traffic | 95

Report: "Smoke coming from warehouse in Industrial Zone B, flames visible"
→ Fire | 98

Report: "Broken street light on Road 45, creating dark spots at night"
→ Public Safety | 85

Report: "Oil spill from parked truck leaking into drainage"
→ Environmental | 90

Report: "Sparks and smoke seen coming from electrical panel in building basement"
→ Fire | 92

Now classify:
Report: "{report}"
→"""

    response = client.chat.completions.create(
        model="gpt-4o-mini", temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


print("=" * 60)
print("ZERO-SHOT vs FEW-SHOT CLASSIFICATION")
print("=" * 60)
print()
print(f"Ambiguous Report:")
print(f'  "{AMBIGUOUS_REPORT}"')
print()
print("  (Could be Fire? Public Safety? Environmental?)")
print()

# Zero-shot
print("--- ZERO-SHOT (no examples) ---")
result_zero = classify_zero_shot(AMBIGUOUS_REPORT)
print(f"  Result: {result_zero}")
print()

# Few-shot
print("--- FEW-SHOT (5 examples provided) ---")
result_few = classify_few_shot(AMBIGUOUS_REPORT)
print(f"  Result: {result_few}")
print()

print("=" * 60)
print("Few-shot gives consistent, confident results because")
print("the model LEARNED the classification pattern from examples.")
print("No training needed. No code. Just examples in the prompt.")
print("=" * 60)
print()

# --- TRY YOUR OWN ---
print("YOUR TURN: Change AMBIGUOUS_REPORT to your own text and run again!")
