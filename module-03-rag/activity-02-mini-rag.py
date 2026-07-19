"""
Module 03 - Activity 2: Build a Mini RAG System
=================================================
A complete RAG pipeline in ~80 lines.
Stores incident reports → searches by meaning → answers from real data.

Run: python activity-02-mini-rag.py
Requires: OPENAI_API_KEY environment variable, chromadb
Install: pip install chromadb
"""

from openai import OpenAI
import chromadb

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# ============================================================
# STEP 1: Create sample incident reports (your "database")
# ============================================================

INCIDENT_REPORTS = [
    {"id": "IR-001", "text": "Vehicle collision on Highway 7, two cars, one driver with neck pain. Time: 08:45. Location: Highway 7 Exit 3."},
    {"id": "IR-002", "text": "Fire reported in warehouse Zone B, heavy smoke visible. Firefighters dispatched. Time: 14:20. Location: Industrial Zone B."},
    {"id": "IR-003", "text": "Stolen motorcycle from parking lot near City Mall. Owner reported at 16:00. Location: City Mall parking."},
    {"id": "IR-004", "text": "Traffic accident on Main Street, truck hit a pedestrian. Serious injuries, ambulance called. Time: 09:15. Location: Main Street."},
    {"id": "IR-005", "text": "Broken water pipe flooding the road on Street 45. Traffic diverted. Time: 11:30. Location: Street 45."},
    {"id": "IR-006", "text": "House fire on Palm Road, family evacuated safely. Fire department on scene. Time: 03:00. Location: Palm Road, Block 7."},
    {"id": "IR-007", "text": "Car theft reported from residential area. CCTV footage available. Time: 22:00. Location: Al Khoud residential."},
    {"id": "IR-008", "text": "Oil spill from delivery truck on Ring Road. Environmental team notified. Time: 13:45. Location: Ring Road near bridge."},
    {"id": "IR-009", "text": "Multiple vehicle pile-up on the expressway during fog. 5 cars involved, 3 minor injuries. Time: 06:30. Location: Expressway KM 45."},
    {"id": "IR-010", "text": "Suspicious package found near government building entrance. Area cordoned off. Time: 10:00. Location: Government District."},
]

# ============================================================
# STEP 2: Store in vector database (ChromaDB)
# ============================================================

print("=" * 60)
print("MINI RAG SYSTEM - Building...")
print("=" * 60)
print()

# Create local vector DB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="incidents",
    metadata={"hnsw:space": "cosine"}
)

# Add all reports
print(f"Storing {len(INCIDENT_REPORTS)} incident reports in vector database...")
collection.add(
    documents=[r["text"] for r in INCIDENT_REPORTS],
    ids=[r["id"] for r in INCIDENT_REPORTS]
)
print("  Done! All reports embedded and stored.")
print()

# ============================================================
# STEP 3: RAG Function - Search + Generate
# ============================================================

def ask_rag(question, n_results=3):
    """Complete RAG pipeline: search → retrieve → generate."""

    # Search for relevant documents
    results = collection.query(query_texts=[question], n_results=n_results)
    retrieved_docs = results["documents"][0]
    retrieved_ids = results["ids"][0]

    # Build context from retrieved documents
    context = "\n".join([
        f"[{rid}]: {doc}"
        for rid, doc in zip(retrieved_ids, retrieved_docs)
    ])

    # Generate answer grounded in retrieved documents
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": """You are an incident report analyst.
Answer questions ONLY based on the provided documents.
If the answer is not in the documents, say "Information not available in current data."
Always reference which report ID(s) your answer is based on."""},
            {"role": "user", "content": f"""RETRIEVED DOCUMENTS:
{context}

QUESTION: {question}

Answer based ONLY on the documents above:"""}
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": retrieved_ids,
        "retrieved_docs": retrieved_docs
    }


# ============================================================
# STEP 4: Test it!
# ============================================================

QUESTIONS = [
    "What traffic accidents happened this week?",
    "Were there any fires reported?",
    "Any incidents involving theft?",
    "What happened on Highway 7?",
    "How many earthquakes were reported?",  # Not in data!
]

print("=" * 60)
print("TESTING RAG SYSTEM")
print("=" * 60)

for q in QUESTIONS:
    print(f"\nQ: {q}")
    print("-" * 40)
    result = ask_rag(q)
    print(f"A: {result['answer']}")
    print(f"Sources: {result['sources']}")
    print()

print("=" * 60)
print("KEY POINTS:")
print("  1. Answers come from REAL data (no hallucination)")
print("  2. Sources are always cited (auditable)")
print("  3. Unknown info → 'Not available' (honest)")
print("  4. Semantic search finds meaning, not keywords")
print()
print("TRY: Add your own question or modify the reports!")
print("=" * 60)
