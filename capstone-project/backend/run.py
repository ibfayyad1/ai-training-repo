"""
Run the Flask Application
=========================
Start the backend server.

Usage:
  python run.py

The server will start at: http://localhost:5000
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("  Incident Report System - Backend API")
    print("  Running at: http://localhost:5001")
    print("=" * 50)
    app.run(debug=True, port=5001)
