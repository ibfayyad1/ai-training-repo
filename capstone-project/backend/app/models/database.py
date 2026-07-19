"""
Database Layer (Model)
======================
SQLite database for storing incidents and users.

This is the DATA layer - where all incidents are stored and retrieved.
In a production system, this would be PostgreSQL or similar.
For our training, SQLite keeps it simple (single file, no server needed).
"""

import sqlite3
import os
from datetime import datetime


DATABASE_PATH = 'incidents.db'


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def init_db(app=None):
    """Create tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    # Users table (simple - no real auth, just roles)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('reporter', 'admin')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Incidents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_number TEXT UNIQUE NOT NULL,
            reporter_username TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            severity TEXT,
            location TEXT,
            timestamp_extracted TEXT,
            image_path TEXT,
            image_analysis TEXT,
            ai_report TEXT,
            ai_reasoning TEXT,
            confidence INTEGER,
            status TEXT DEFAULT 'open' CHECK(status IN ('open', 'reviewing', 'resolved', 'closed')),
            pdf_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reporter_username) REFERENCES users(username)
        )
    ''')

    # Insert default users
    cursor.execute("INSERT OR IGNORE INTO users (username, role) VALUES ('admin', 'admin')")
    cursor.execute("INSERT OR IGNORE INTO users (username, role) VALUES ('reporter1', 'reporter')")
    cursor.execute("INSERT OR IGNORE INTO users (username, role) VALUES ('reporter2', 'reporter')")

    conn.commit()
    conn.close()


# ============================================================
# CRUD Operations
# ============================================================

def create_incident(data):
    """Save a new incident to the database."""
    conn = get_db()
    cursor = conn.cursor()

    # Generate report number
    cursor.execute("SELECT COUNT(*) FROM incidents")
    count = cursor.fetchone()[0]
    report_number = f"IR-{count + 1001:04d}"

    cursor.execute('''
        INSERT INTO incidents (
            report_number, reporter_username, description, category,
            severity, location, timestamp_extracted, image_path,
            image_analysis, ai_report, ai_reasoning, confidence, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        report_number,
        data.get('reporter_username', 'reporter1'),
        data['description'],
        data.get('category'),
        data.get('severity'),
        data.get('location'),
        data.get('timestamp_extracted'),
        data.get('image_path'),
        data.get('image_analysis'),
        data.get('ai_report'),
        data.get('ai_reasoning'),
        data.get('confidence'),
        'open'
    ))

    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()

    return {"id": incident_id, "report_number": report_number}


def get_all_incidents(filters=None):
    """Get all incidents with optional filters."""
    conn = get_db()
    query = "SELECT * FROM incidents"
    params = []
    conditions = []

    if filters:
        if filters.get('category'):
            conditions.append("category = ?")
            params.append(filters['category'])
        if filters.get('severity'):
            conditions.append("severity = ?")
            params.append(filters['severity'])
        if filters.get('status'):
            conditions.append("status = ?")
            params.append(filters['status'])
        if filters.get('reporter_username'):
            conditions.append("reporter_username = ?")
            params.append(filters['reporter_username'])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC"

    results = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_incident_by_id(incident_id):
    """Get a single incident by ID."""
    conn = get_db()
    result = conn.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
    conn.close()
    return dict(result) if result else None


def get_incident_by_report_number(report_number):
    """Get a single incident by report number."""
    conn = get_db()
    result = conn.execute("SELECT * FROM incidents WHERE report_number = ?", (report_number,)).fetchone()
    conn.close()
    return dict(result) if result else None


def update_incident_status(incident_id, status):
    """Update incident status."""
    conn = get_db()
    conn.execute(
        "UPDATE incidents SET status = ?, updated_at = ? WHERE id = ?",
        (status, datetime.now().isoformat(), incident_id)
    )
    conn.commit()
    conn.close()


def update_incident_pdf(incident_id, pdf_path):
    """Update incident with PDF path."""
    conn = get_db()
    conn.execute(
        "UPDATE incidents SET pdf_path = ? WHERE id = ?",
        (pdf_path, incident_id)
    )
    conn.commit()
    conn.close()


def get_stats():
    """Get incident statistics for the dashboard."""
    conn = get_db()

    stats = {
        "total": conn.execute("SELECT COUNT(*) FROM incidents").fetchone()[0],
        "by_category": {},
        "by_severity": {},
        "by_status": {},
        "this_week": conn.execute(
            "SELECT COUNT(*) FROM incidents WHERE created_at >= date('now', '-7 days')"
        ).fetchone()[0],
        "this_month": conn.execute(
            "SELECT COUNT(*) FROM incidents WHERE created_at >= date('now', '-30 days')"
        ).fetchone()[0],
    }

    # By category
    rows = conn.execute("SELECT category, COUNT(*) as count FROM incidents GROUP BY category").fetchall()
    stats["by_category"] = {row["category"]: row["count"] for row in rows if row["category"]}

    # By severity
    rows = conn.execute("SELECT severity, COUNT(*) as count FROM incidents GROUP BY severity").fetchall()
    stats["by_severity"] = {row["severity"]: row["count"] for row in rows if row["severity"]}

    # By status
    rows = conn.execute("SELECT status, COUNT(*) as count FROM incidents GROUP BY status").fetchall()
    stats["by_status"] = {row["status"]: row["count"] for row in rows if row["status"]}

    conn.close()
    return stats
