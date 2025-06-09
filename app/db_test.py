
from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text

db_test_bp = Blueprint('db_test', __name__)

@db_test_bp.route('/api/db-test')
def db_test():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "message": "Database is connected"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Database error: {str(e)}"})
