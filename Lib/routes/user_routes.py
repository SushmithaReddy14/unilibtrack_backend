from flask import Blueprint, jsonify, request
from db_config import get_db_connection

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/get_user', methods=['GET'])
def get_user():
    data = request.get_json()
    user_id = data.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    return jsonify(user or {"message": "User not found"})
