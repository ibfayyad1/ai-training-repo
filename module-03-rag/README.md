# Module 03 - RAG & Knowledge Systems

## Activities

| # | File | What You Learn |
|---|------|---------------|
| 1 | `activity-01-embeddings.py` | How AI understands meaning using vectors |
| 2 | `activity-02-mini-rag.py` | Build a complete RAG system (~80 lines) |
| 3 | `activity-03-rag-vs-no-rag.py` | See hallucination vs grounded answers |

## Setup

```bash
pip install openai chromadb
export OPENAI_API_KEY="your-key"
```

## Run

```bash
python activity-01-embeddings.py     # See similarity scores
python activity-02-mini-rag.py       # Full RAG pipeline
python activity-03-rag-vs-no-rag.py  # Side-by-side comparison
```

## Key Concepts

- **Embeddings**: Text → numbers (vectors) that capture meaning
- **Vector DB**: Storage that enables search by meaning
- **RAG Pipeline**: Question → Search → Retrieve → Generate (grounded)
- **Why not fine-tuning?**: RAG is cheaper, faster, updatable, auditable
