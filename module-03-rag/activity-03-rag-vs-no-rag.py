"""
Module 03 - Activity 3: RAG vs No-RAG Comparison
==================================================
Same question. Two approaches.
See hallucination vs grounded answers.

Run: python activity-03-rag-vs-no-rag.py
Requires: OPENAI_API_KEY environment variable, chromadb
"""

from openai import OpenAI
import chromadb

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# --- Setup mini database ---
REPORTS = [
    "IR-001: Traffic accident Highway 7, 2 cars, minor injuries. July 14.",
    "IR-002: Traffic accident Main Street, truck vs pedestrian, serious. July 14.",
    "IR-003: Fire in warehouse Zone B, no injuries. July 13.",
    "IR-004: Traffic accident Ring Road, 3 cars, 1 minor injury. July 15.",
    "IR-005: Theft at electronics store, forced entry. July 12.",
    "IR-006: Traffic accident Expressway, fog, 5 cars. July 15.",
    "IR-007: Environmental spill, oil on road. July 13.",
]

# Vector DB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("comparison_test")
collection.add(
    documents=REPORTS,
    ids=[f"doc-{i}" for i in range(len(REPORTS))]
)

QUESTION = "How many traffic accidents happened this week? What was the most serious one?"

print("=" * 60)
print("RAG vs NO-RAG - Same Question, Different Approaches")
print("=" * 60)
print()
print(f"Question: {QUESTION}")
print()

# --- NO RAG ---
print("=" * 60)
print("WITHOUT RAG (AI answers from memory)")
print("=" * 60)
print()

response_no_rag = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    messages=[{"role": "user", "content": QUESTION}]
)
print(response_no_rag.choices[0].message.content)
print()
print("  ⚠️  These numbers are INVENTED. The AI has no data.")
print()

# --- WITH RAG ---
print("=" * 60)
print("WITH RAG (AI answers from retrieved documents)")
print("=" * 60)
print()

# Retrieve relevant docs
results = collection.query(query_texts=[QUESTION], n_results=5)
context = "\n".join(results["documents"][0])

response_rag = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role": "system", "content": "Answer ONLY from provided documents. Cite report IDs. If not in data, say 'Not available'."},
        {"role": "user", "content": f"DOCUMENTS:\n{context}\n\nQUESTION: {QUESTION}"}
    ]
)
print(response_rag.choices[0].message.content)
print()
print("  ✓  Every fact comes from real reports. Citations included.")
print()

print("=" * 60)
print("THE DIFFERENCE:")
print("  No RAG  → Confident but FAKE numbers")
print("  RAG     → Accurate, cited, honest about limits")
print()
print("  This is why RAG is essential for any system")
print("  where correctness matters.")
print("=" * 60)
print()
print("YOUR TURN: Change the QUESTION variable at the top and run again.")
print("Try: 'Were there any fires?' or 'What happened on the Ring Road?'")
