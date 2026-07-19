"""
Module 03 - Activity 1: Understanding Embeddings
==================================================
See how AI converts text into numbers (vectors)
and finds similar meanings.

Run: python activity-01-embeddings.py
Requires: OPENAI_API_KEY environment variable
"""

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()


def get_embedding(text):
    """Get embedding vector for a text."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(a, b):
    """Calculate similarity between two vectors (0=different, 1=identical)."""
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    return dot_product / (norm_a * norm_b)


# --- INCIDENT REPORTS ---

reports = {
    "A": "Vehicle collision on the highway, two cars involved, minor injuries",
    "B": "Traffic accident on the main road, car crash, one person hurt",
    "C": "Fire broke out in a warehouse, firefighters dispatched",
    "D": "Stolen laptop reported from office building on 3rd floor",
    "E": "تصادم مركبات على الطريق السريع، إصابات طفيفة",  # Arabic = same as A
}

print("=" * 60)
print("EMBEDDING SIMILARITY - Same Meaning vs Different Meaning")
print("=" * 60)
print()
print("Reports:")
for key, text in reports.items():
    print(f"  {key}: {text[:60]}...")
print()

# Get embeddings
print("Getting embeddings...")
embeddings = {key: get_embedding(text) for key, text in reports.items()}
print(f"  Each embedding = {len(embeddings['A'])} numbers (dimensions)")
print()

# Compare similarities
print("=" * 60)
print("SIMILARITY SCORES (1.0 = identical meaning, 0.0 = unrelated)")
print("=" * 60)
print()

comparisons = [
    ("A", "B", "EN collision vs EN accident (same meaning!)"),
    ("A", "E", "EN collision vs AR collision (same meaning, different language!)"),
    ("A", "C", "EN collision vs EN fire (different type)"),
    ("A", "D", "EN collision vs EN theft (completely different)"),
    ("C", "D", "EN fire vs EN theft (both different from traffic)"),
]

for key1, key2, description in comparisons:
    sim = cosine_similarity(embeddings[key1], embeddings[key2])
    bar = "█" * int(sim * 30)
    print(f"  {key1} vs {key2}: {sim:.3f}  {bar}")
    print(f"           {description}")
    print()

print("=" * 60)
print("KEY INSIGHT:")
print("  - Same meaning (different words) = HIGH similarity")
print("  - Same meaning (different language!) = HIGH similarity")
print("  - Different topics = LOW similarity")
print()
print("  This is how RAG finds relevant reports - by MEANING,")
print("  not by matching exact keywords.")
print("=" * 60)
