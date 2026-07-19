"""
Stats Controller - Dashboard Statistics & PDF Downloads
========================================================
Endpoints for the dashboard and file downloads.

ENDPOINTS:
  GET /api/stats              → Dashboard statistics
  GET /api/pdf/<report_num>   → Download incident PDF
"""

import os
from flask import Blueprint, request, jsonify, send_file
from app.models.database import get_stats, get_incident_by_id, get_incident_by_report_number
from app.services.pdf_service import generate_incident_pdf

stats_bp = Blueprint('stats', __name__)


# ============================================================
# GET /api/stats - Dashboard Statistics
# ============================================================

@stats_bp.route('/api/stats', methods=['GET'])
def dashboard_stats():
    """
    Get incident statistics for the admin dashboard.

    Returns:
      - total: total incident count
      - by_category: count per category
      - by_severity: count per severity
      - by_status: count per status
      - this_week: incidents in last 7 days
      - this_month: incidents in last 30 days
    """
    stats = get_stats()
    return jsonify(stats)


# ============================================================
# GET /api/pdf/<id> - Download Incident PDF
# ============================================================

@stats_bp.route('/api/pdf/<int:incident_id>', methods=['GET'])
def download_pdf(incident_id):
    """
    Download (or generate) PDF for an incident.

    If PDF already exists → serve it.
    If not → generate it first, then serve.
    """
    incident = get_incident_by_id(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404

    # Check if PDF already exists
    pdf_path = incident.get('pdf_path')

    if not pdf_path or not os.path.exists(pdf_path):
        # Generate PDF on the fly
        output_dir = os.path.join(os.getcwd(), 'reports')
        pdf_path = generate_incident_pdf(incident, output_dir=output_dir)
        # Update DB
        from app.models.database import update_incident_pdf
        update_incident_pdf(incident_id, pdf_path)

    return send_file(
        os.path.abspath(pdf_path),
        as_attachment=True,
        download_name=f"report_{incident['report_number']}.pdf",
        mimetype='application/pdf'
    )


# ============================================================
# GET /api/users - Simple user list (for login dropdown)
# ============================================================

@stats_bp.route('/api/users', methods=['GET'])
def get_users():
    """Get list of users (for simple login selection)."""
    from app.models.database import get_db
    conn = get_db()
    users = conn.execute("SELECT username, role FROM users").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])
