"""
Incident Report System - Flask Application Factory
===================================================
This is the main entry point for our Flask backend.
It uses the Factory Pattern to create and configure the app.
"""

from flask import Flask, render_template
from flask_cors import CORS
from app.models.database import init_db
from app.routes import register_routes


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Allow Angular frontend to make API calls
    CORS(app)

    # Configuration
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['REPORTS_FOLDER'] = 'reports'
    app.config['DATABASE'] = 'incidents.db'

    # Initialize database
    init_db(app)

    # Register all API routes
    register_routes(app)

    # Serve frontend
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
