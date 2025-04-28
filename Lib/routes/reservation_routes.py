from flask import Blueprint, jsonify, request, session
from db_config import get_db_connection

reservation_bp = Blueprint('reservation_bp', __name__)

@reservation_bp.route('/reserve_book', methods=['POST'])
def reserve_book():
    print('userId:', session.get('username'))
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = session.get('user_id')
    username = session.get('username')

    data = request.get_json()
    book_id = data['book_id']
    book_name = data['book_name']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Reservations (user_id, book_id, username, book_name)
        VALUES (%s, %s, %s, %s)
    """, (user_id, book_id, username, book_name))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book reserved successfully"})

@reservation_bp.route('/get_all_reservations', methods= ['GET'])
def get_all_reservations():
    if 'user_id' not in session:
        return jsonify({"message" : "Unauthorized"}), 401
    
    user_id = session.get('user_id')
    print('getREservstuions userid: ', user_id)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(" SELECT * FROM reservations")
    reservations = cursor.fetchall()
    conn.commit()
    conn.close()
    return jsonify(reservations or {"message" : "Reservations not found"})

@reservation_bp.route('/get_user_reservations', methods= ['GET'])
def get_user_reservations():
    if 'user_id' not in session:
        return jsonify({"message" : "Unauthorized"}), 401
    
    user_id = session.get('user_id')
    print('getREservstuions userid: ', user_id)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(" SELECT * FROM reservations WHERE user_id = %s", (user_id,))
    reservations = cursor.fetchall()
    conn.commit()
    conn.close()
    return jsonify(reservations or {"message" : "Reservations not found"})

@reservation_bp.route('/cancel_reserv', methods= ['POST'])
def cancel_reservation():
    if 'user_id' not in session:
        return jsonify({"message" : "Unauthorized"}), 401
    
    user_id = session.get('user_id')

    data = request.get_json()
    book_id = data['book_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE reservations SET status = 'Cancelled' WHERE user_id = %s AND book_id = %s
    """, (user_id, book_id))
    reservations = cursor.fetchall()
    conn.commit()
    conn.close()
    return jsonify(reservations or {"message" : "Reservations not found"})

