"""
Module 02 - Activity 3: Chain of Thought
==========================================
Force AI to reason step-by-step.
Better accuracy + explainable decisions.

Run: python activity-03-chain-of-thought.py
Requires: OPENAI_API_KEY environment variable
"""

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

REPORT = "Two trucks collided on the highway. Fuel is leaking onto the road. One driver complaining of back pain. Road blocked in both directions."


def assess_without_cot(report):
    """Quick assessment - no reasoning required."""
    prompt = f"""What is the severity of this incident? 
Answer with one word: low, medium, high, or critical.

Report: "{report}"
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini", temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def assess_with_cot(report):
    """Step-by-step assessment - forced reasoning."""
    prompt = f"""Assess the severity of this incident. Think through these steps:

1. INCIDENT TYPE: What kind of incident is this?
2. INJURIES: Are there injuries or risk to life?
3. ONGOING DANGER: Is there continuing danger to the public?
4. RESOURCES NEEDED: What response is required?
5. FINAL SEVERITY: Based on steps 1-4, assign: low / medium / high / critical
6. JUSTIFICATION: One sentence explaining why.

Report: "{report}"

Think step by step:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini", temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


print("=" * 60)
print("CHAIN OF THOUGHT: Same report, two approaches")
print("=" * 60)
print()
print(f"Report: {REPORT}")
print()

# Without CoT
print("--- WITHOUT Chain of Thought ---")
result_no_cot = assess_without_cot(REPORT)
print(f"  Answer: {result_no_cot}")
print(f"  (No explanation. No reasoning. Cannot audit.)")
print()

# With CoT
print("--- WITH Chain of Thought ---")
result_cot = assess_with_cot(REPORT)
print(f"  {result_cot}")
print()

print("=" * 60)
print("WITH CoT: You get full reasoning → auditable decisions.")
print("If step 2 reasoning is wrong, you catch the error BEFORE")
print("it reaches the final severity assessment.")
print("=" * 60)
print()

# --- TRY AMBIGUOUS CASE ---
print()
print("--- BONUS: Try this ambiguous report ---")
AMBIGUOUS = "Unattended bag found near shopping mall entrance during peak hours"
print(f'  "{AMBIGUOUS}"')
print()
print("  Run with CoT - see how it reasons through the ambiguity.")
result_ambiguous = assess_with_cot(AMBIGUOUS)
print(f"  {result_ambiguous}")
