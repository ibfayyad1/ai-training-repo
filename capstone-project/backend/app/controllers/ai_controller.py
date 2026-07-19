"""
AI Controller - AI-powered features (RAG Q&A, Analytics, Reports)
==================================================================
Handles all AI-specific endpoints that aren't part of basic CRUD.

ENDPOINTS:
  POST /api/ai/ask          → RAG-powered Q&A (Module 03)
  POST /api/ai/analytics    → AI pattern detection (Module 01+02+03)
  POST /api/ai/monthly      → Generate monthly report (Module 01+02)
  GET  /api/ai/rebuild-rag  → Rebuild RAG index
"""

import json
from flask import Blueprint, request, jsonify
from app.models.database import get_all_incidents, get_stats
from app.services.rag_service import ask_ai, rebuild_index
from app.services.ai_service import analyze_patterns, generate_monthly_report
from app.services.pdf_service import generate_monthly_pdf

ai_bp = Blueprint('ai', __name__)


# ============================================================
# POST /api/ai/ask - RAG-Powered Q&A (Module 03)
# Admin asks any question → AI answers from REAL data
# ============================================================

@ai_bp.route('/api/ai/ask', methods=['POST'])
def ask_question():
    """
    Ask AI a question - answered using RAG (Module 03).

    HOW IT WORKS:
    1. User question → converted to embedding
    2. Vector DB searched for relevant incidents
    3. Retrieved incidents added to AI context
    4. AI answers ONLY from real data (no hallucination)
    5. Sources cited in response

    Request body (JSON):
      - question: string (the question to ask)

    Example questions:
      - "How many traffic accidents this week?"
      - "What's the most common incident type?"
      - "Any patterns in nighttime incidents?"
    """
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Question is required"}), 400

    question = data['question']

    # ---- RAG PIPELINE (Module 03) ----
    result = ask_ai(question)

    return jsonify({
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"],
        "documents_searched": result["documents_used"],
        "technique": "RAG (Retrieval-Augmented Generation) - Module 03"
    })


# ============================================================
# POST /api/ai/analytics - AI Pattern Detection
# AI analyzes all incidents and finds patterns
# ============================================================

@ai_bp.route('/api/ai/analytics', methods=['POST'])
def get_analytics():
    """
    AI analyzes recent incidents to find patterns and insights.

    TECHNIQUES USED:
    - Context Window (Module 01): Feed multiple incidents for cross-analysis
    - Chain of Thought (Module 02): Step-by-step pattern detection
    - RAG (Module 03): Retrieves relevant data first
    - Grounding (Module 02): Only from provided data

    Request body (JSON, optional):
      - days: number of days to analyze (default: 30)
    """
    data = request.get_json() or {}
    days = data.get('days', 30)

    # Get recent incidents
    incidents = get_all_incidents()

    if not incidents:
        return jsonify({
            "analysis": "No incidents in the database yet. Submit some reports first.",
            "incident_count": 0
        })

    # ---- AI ANALYTICS (Module 01 + 02) ----
    analysis = analyze_patterns(incidents)

    return jsonify({
        "analysis": analysis,
        "incident_count": len(incidents),
        "period_days": days,
        "technique": "Context Window + Chain of Thought - Module 01 & 02"
    })


# ============================================================
# POST /api/ai/monthly - Generate Monthly Report PDF
# Full monthly report with stats, trends, recommendations
# ============================================================

@ai_bp.route('/api/ai/monthly', methods=['POST'])
def monthly_report():
    """
    Generate a comprehensive monthly report (PDF).

    TECHNIQUES USED:
    - Large Context (Module 01): All month's incidents in context
    - Structured Output (Module 02): Executive report format
    - Temperature 0.3 (Module 01): Professional writing style
    - PDF Generation: ReportLab converts to downloadable PDF

    Request body (JSON, optional):
      - month: string (e.g., "2024-07", default: current month)
    """
    data = request.get_json() or {}
    month = data.get('month', 'current')

    # Get all incidents and stats
    incidents = get_all_incidents()
    stats = get_stats()

    if not incidents:
        return jsonify({"error": "No incidents to report on"}), 400

    # ---- GENERATE REPORT TEXT (Module 01 + 02) ----
    report_text = generate_monthly_report(incidents, stats)

    # ---- GENERATE PDF ----
    pdf_path = generate_monthly_pdf(report_text, month, stats)

    return jsonify({
        "success": True,
        "report_text": report_text,
        "pdf_path": pdf_path,
        "stats": stats,
        "incidents_analyzed": len(incidents),
        "technique": "Large Context + Structured Generation - Module 01 & 02"
    })


# ============================================================
# GET /api/ai/rebuild-rag - Rebuild Vector Database
# Re-indexes all incidents for RAG search
# ============================================================

@ai_bp.route('/api/ai/rebuild-rag', methods=['GET'])
def rebuild_rag():
    """
    Rebuild the RAG vector database from all stored incidents.
    Call this after importing data or if search seems off.
    """
    result = rebuild_index()
    return jsonify({
        "success": True,
        "message": f"RAG index rebuilt. {result['indexed']} incidents indexed.",
        "indexed": result['indexed']
    })
