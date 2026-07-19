"""
RAG Service - Retrieval-Augmented Generation (Module 03)
=========================================================
This connects the AI to your REAL incident database.
Instead of the AI inventing answers, it SEARCHES for real data first.

MODULE 03 CONCEPTS DEMONSTRATED:
┌──────────────────────────────────────────────────────────────────┐
│ • Embeddings: Convert text to vectors that capture meaning       │
│ • Vector Database: ChromaDB stores and searches by meaning       │
│ • Semantic Search: Find relevant reports by MEANING not keywords │
│ • Grounded Generation: AI answers ONLY from retrieved data       │
│ • Citations: AI references which reports it used                 │
│ • "Not Available": AI admits when data doesn't exist             │
└──────────────────────────────────────────────────────────────────┘

THE RAG PIPELINE (6 steps):
1. User asks a question
2. Question is converted to embedding (vector)
3. Vector DB finds most similar documents
4. Retrieved documents are added to the prompt
5. LLM generates answer ONLY from those documents
6. Response includes citations to source reports
"""

import json
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# ============================================================
# VECTOR DATABASE SETUP (ChromaDB)
# ChromaDB stores embeddings locally - no cloud needed.
# Each incident report is converted to a vector and stored here.
# ============================================================

chroma_client = chromadb.Client()

# Create or get the collection
try:
    collection = chroma_client.get_collection("incidents")
except Exception:
    collection = chroma_client.create_collection(
        name="incidents",
        metadata={"hnsw:space": "cosine"}  # Use cosine similarity
    )


# ============================================================
# 1. INDEX AN INCIDENT (add to vector DB)
#    Called every time a new incident is saved.
#    Technique: Convert text → embedding → store
# ============================================================

def index_incident(incident: dict):
    """
    Add an incident to the vector database for future search.

    TECHNIQUE (Module 03 - Embeddings):
    Text → vector of 1536 numbers that captures MEANING.
    "car crash" and "vehicle collision" will have similar vectors
    even though the words are different.
    """
    # Build the document text (what we embed)
    doc_text = (
        f"Report {incident.get('report_number', 'N/A')}: "
        f"{incident.get('category', '')} incident. "
        f"Severity: {incident.get('severity', '')}. "
        f"Location: {incident.get('location', '')}. "
        f"Description: {incident.get('description', '')}. "
        f"Date: {incident.get('created_at', '')[:10]}"
    )

    # Add to ChromaDB (it handles embedding automatically)
    collection.add(
        documents=[doc_text],
        ids=[str(incident.get('id', incident.get('report_number', 'unknown')))],
        metadatas=[{
            "report_number": incident.get("report_number", ""),
            "category": incident.get("category", ""),
            "severity": incident.get("severity", ""),
            "location": incident.get("location", ""),
            "date": incident.get("created_at", "")[:10] if incident.get("created_at") else ""
        }]
    )


# ============================================================
# 2. SEARCH INCIDENTS BY MEANING (semantic search)
#    User asks a question → we find the most relevant reports.
#    Technique: Query embedding → cosine similarity search
# ============================================================

def search_incidents(query: str, n_results: int = 5) -> list:
    """
    Search incidents by meaning (semantic search).

    TECHNIQUE (Module 03 - Vector Search):
    The query "traffic accidents near the highway" will find reports
    about "vehicle collision on Highway 7" - because they MEAN the same thing.
    Keyword search would MISS this because the words are different.

    Returns: list of relevant documents with metadata
    """
    # Check if collection has any documents
    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    # Format results
    documents = []
    for i in range(len(results["documents"][0])):
        documents.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
            "id": results["ids"][0][i]
        })

    return documents


# ============================================================
# 3. RAG-POWERED Q&A (the full pipeline)
#    User asks any question → search → grounded answer
#    This is the "Ask AI" feature for admins.
# ============================================================

def ask_ai(question: str) -> dict:
    """
    Answer a question using RAG - grounded in real incident data.

    THE FULL RAG PIPELINE (Module 03):
    ┌─────────────────────────────────────────────────────────┐
    │ Step 1: User asks: "How many fires this week?"          │
    │ Step 2: Convert question to embedding                    │
    │ Step 3: Search vector DB → find 5 most relevant reports │
    │ Step 4: Build prompt with retrieved documents            │
    │ Step 5: LLM answers ONLY from those documents           │
    │ Step 6: Include citations (which reports used)           │
    └─────────────────────────────────────────────────────────┘

    TECHNIQUES USED:
    • Semantic Search (Module 03): Find by meaning
    • Grounding Prompt (Module 02): "Only answer from provided data"
    • Citations (Module 02): Reference source reports
    • Temperature 0 (Module 01): Factual, no hallucination
    """

    # Step 2-3: Search for relevant documents
    relevant_docs = search_incidents(question, n_results=7)

    if not relevant_docs:
        return {
            "answer": "No incident data available yet. Please submit some reports first.",
            "sources": [],
            "documents_used": 0
        }

    # Step 4: Build context from retrieved documents
    context = "\n".join([
        f"[{doc['metadata'].get('report_number', doc['id'])}]: {doc['text']}"
        for doc in relevant_docs
    ])

    # Step 5: Send to LLM with grounding instructions
    # ---- SYSTEM PROMPT (Module 02: Grounding + Citations) ----
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,           # Module 01: No hallucination - factual only
        max_tokens=500,
        messages=[
            {"role": "system", "content": """You are an incident data analyst.
Answer questions ONLY based on the provided incident reports.

RULES:
- ONLY use information from the provided documents
- If the answer is NOT in the documents, say: "This information is not available in the current data."
- ALWAYS cite which report numbers you used (e.g., "Based on IR-1001, IR-1003...")
- Give specific numbers and facts from the documents
- If asked for counts, count from the documents provided
- Respond in the same language as the question"""},
            {"role": "user", "content": f"""RETRIEVED DOCUMENTS:
{context}

QUESTION: {question}

Answer based ONLY on the documents above. Cite your sources."""}
        ]
    )

    # Step 6: Return answer with sources
    sources = [doc['metadata'].get('report_number', doc['id']) for doc in relevant_docs]

    return {
        "answer": response.choices[0].message.content,
        "sources": sources,
        "documents_used": len(relevant_docs)
    }


# ============================================================
# 4. REBUILD INDEX (re-index all incidents from database)
#    Called at startup or when data is refreshed.
# ============================================================

def rebuild_index():
    """
    Rebuild the entire vector database from SQLite data.
    Called at server startup to ensure RAG is up-to-date.
    """
    from app.models.database import get_all_incidents

    # Clear existing collection
    global collection
    try:
        chroma_client.delete_collection("incidents")
    except Exception:
        pass
    collection = chroma_client.create_collection(
        name="incidents",
        metadata={"hnsw:space": "cosine"}
    )

    # Re-index all incidents
    incidents = get_all_incidents()
    for incident in incidents:
        index_incident(incident)

    return {"indexed": len(incidents)}
