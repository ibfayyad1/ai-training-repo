"""
Module 01 - Activity 2: Temperature Effect
============================================
Same classification prompt, different temperatures.
See how temperature affects consistency.

Run: python activity-02-temperature.py
Requires: OPENAI_API_KEY environment variable
"""

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

REPORT = "Loud noises and suspicious activity reported near a warehouse at midnight, neighbors concerned about safety"

PROMPT = f"""Classify this incident into exactly ONE category:
- Traffic
- Fire
- Theft
- Public Safety
- Environmental

Report: "{REPORT}"

Respond with only the category name."""


def classify_at_temperature(temp, runs=3):
    """Run classification multiple times at given temperature."""
    results = []
    for i in range(runs):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=temp,
            max_tokens=20,
            messages=[{"role": "user", "content": PROMPT}]
        )
        answer = response.choices[0].message.content.strip()
        results.append(answer)
    return results


print("=" * 60)
print("TEMPERATURE EXPERIMENT: Same report, classified 3 times")
print("=" * 60)
print()
print(f'Report: "{REPORT[:60]}..."')
print()

# Temperature 0
print("--- Temperature = 0 (deterministic) ---")
results_0 = classify_at_temperature(0.0)
for i, r in enumerate(results_0, 1):
    print(f"  Run {i}: {r}")
print(f"  Consistent? {'YES' if len(set(results_0)) == 1 else 'NO'}")
print()

# Temperature 1.0
print("--- Temperature = 1.0 (random) ---")
results_1 = classify_at_temperature(1.0)
for i, r in enumerate(results_1, 1):
    print(f"  Run {i}: {r}")
print(f"  Consistent? {'YES' if len(set(results_1)) == 1 else 'NO'}")
print()

print("=" * 60)
print("CONCLUSION:")
print("  Temperature 0 → Same answer every time (use for classification)")
print("  Temperature 1 → Different answers (bad for classification!)")
print("=" * 60)
print()
print("=" * 60)
print("YOUR TURN: Change the REPORT variable at the top to your own")
print("incident and run again. Try something ambiguous!")
print("=" * 60)
