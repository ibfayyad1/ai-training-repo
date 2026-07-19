"""
Routes Registration
====================
Register all API blueprints (controllers) with the Flask app.
"""

from app.controllers.incident_controller import incident_bp
from app.controllers.ai_controller import ai_bp
from app.controllers.stats_controller import stats_bp


def register_routes(app):
    """Register all route blueprints."""
    app.register_blueprint(incident_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(stats_bp)
