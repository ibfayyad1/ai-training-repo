"""
Incident Controller - Handles all incident-related API requests
================================================================
This is the CONTROLLER layer (MVC pattern).
It receives HTTP requests, validates input, calls services, and returns responses.

ENDPOINTS:
  POST /api/incidents          → Submit new incident (uses Agent - Module 04)
  GET  /api/incidents          → List incidents (with filters)
  GET  /api/incidents/<id>     → Get single incident detail
  PUT  /api/incidents/<id>     → Update status (Admin only)
"""

import os
import json
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.models.database import (
    get_all_incidents, get_incident_by_id, update_incident_status,
    update_incident_pdf
)
from app.services.agent_service import process_incident_with_agent
from app.services.ai_service import generate_report
from app.services.pdf_service import generate_incident_pdf
from app.services.rag_service import index_incident

incident_bp = Blueprint('incidents', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================================
# POST /api/incidents - Submit New Incident
# Uses: AI AGENT (Module 04) to process the full workflow
# ============================================================

@incident_bp.route('/api/incidents', methods=['POST'])
def submit_incident():
    """
    Submit a new incident report.

    The AI AGENT (Module 04) handles the full workflow:
    1. Classifies the report (Module 02: Few-shot + CoT)
    2. Analyzes image if provided (Vision)
    3. Saves to database
    4. Generates full report (Module 02: Structured generation)
    5. Sends notification if high/critical severity

    Request body (form-data):
      - description: string (required) - the incident report text
      - image: file (optional) - photo of the incident
      - reporter_username: string (optional, default: 'reporter1')
    """
    # Validate input
    description = request.form.get('description')
    if not description:
        return jsonify({"error": "Description is required"}), 400

    reporter = request.form.get('reporter_username', 'reporter1')

    # Handle image upload
    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_dir = os.path.join(os.getcwd(), 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            image_path = os.path.join(upload_dir, filename)
            file.save(image_path)

    # ---- USE AI AGENT (Module 04) ----
    # The agent decides what to do: classify → analyze → save → report → notify
    agent_result = process_incident_with_agent(
        description=description,
        image_path=image_path,
        reporter_username=reporter
    )

    # Generate PDF for the saved incident
    # Find the saved incident from agent actions
    saved_incident = None
    for action in agent_result.get('actions_taken', []):
        if action['tool'] == 'save_incident':
            # Get the incident from DB
            from app.models.database import get_all_incidents
            incidents = get_all_incidents({'reporter_username': reporter})
            if incidents:
                saved_incident = incidents[0]  # Most recent
                break

    # Generate PDF if we have a saved incident
    pdf_path = None
    if saved_incident:
        # Generate AI report text
        classification = {
            'category': saved_incident.get('category'),
            'severity': saved_incident.get('severity'),
            'location': saved_incident.get('location'),
            'timestamp_extracted': saved_incident.get('timestamp_extracted'),
            'confidence': saved_incident.get('confidence'),
            'reasoning': saved_incident.get('ai_reasoning')
        }
        ai_report = generate_report(description, classification, saved_incident.get('image_analysis'))

        # Update DB with report
        from app.models.database import get_db
        conn = get_db()
        conn.execute("UPDATE incidents SET ai_report = ? WHERE id = ?", (ai_report, saved_incident['id']))
        conn.commit()
        conn.close()

        # Generate PDF
        saved_incident['ai_report'] = ai_report
        pdf_path = generate_incident_pdf(saved_incident)
        update_incident_pdf(saved_incident['id'], pdf_path)

        # Index in RAG (Module 03) - so this incident is searchable
        index_incident(saved_incident)

    return jsonify({
        "success": agent_result.get("success", False),
        "message": agent_result.get("final_answer", "Incident processed"),
        "report_number": saved_incident.get("report_number") if saved_incident else None,
        "classification": {
            "category": saved_incident.get("category") if saved_incident else None,
            "severity": saved_incident.get("severity") if saved_incident else None,
        },
        "pdf_available": pdf_path is not None,
        "agent_steps": len(agent_result.get("actions_taken", [])),
        "actions": agent_result.get("actions_taken", [])
    }), 201


# ============================================================
# GET /api/incidents - List All Incidents
# ============================================================

@incident_bp.route('/api/incidents', methods=['GET'])
def list_incidents():
    """
    Get all incidents with optional filters.

    Query params:
      - category: Traffic, Fire, Theft, Public Safety, Environmental
      - severity: low, medium, high, critical
      - status: open, reviewing, resolved, closed
      - reporter_username: filter by reporter
    """
    filters = {}
    if request.args.get('category'):
        filters['category'] = request.args['category']
    if request.args.get('severity'):
        filters['severity'] = request.args['severity']
    if request.args.get('status'):
        filters['status'] = request.args['status']
    if request.args.get('reporter_username'):
        filters['reporter_username'] = request.args['reporter_username']

    incidents = get_all_incidents(filters if filters else None)

    return jsonify({
        "count": len(incidents),
        "incidents": incidents
    })


# ============================================================
# GET /api/incidents/<id> - Get Single Incident
# ============================================================

@incident_bp.route('/api/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    """Get a single incident with all details."""
    incident = get_incident_by_id(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404

    return jsonify(incident)


# ============================================================
# PUT /api/incidents/<id> - Update Status (Admin)
# ============================================================

@incident_bp.route('/api/incidents/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    """
    Update incident status. Admin only.

    Request body (JSON):
      - status: "open" | "reviewing" | "resolved" | "closed"
    """
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({"error": "Status is required"}), 400

    valid_statuses = ['open', 'reviewing', 'resolved', 'closed']
    if data['status'] not in valid_statuses:
        return jsonify({"error": f"Invalid status. Use: {valid_statuses}"}), 400

    incident = get_incident_by_id(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404

    update_incident_status(incident_id, data['status'])

    return jsonify({
        "success": True,
        "message": f"Status updated to '{data['status']}'",
        "incident_id": incident_id
    })
