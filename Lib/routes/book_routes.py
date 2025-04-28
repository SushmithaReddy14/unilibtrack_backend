from flask import Blueprint, jsonify, session
from db_config import get_db_connection

book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/get_books', methods=['GET'])
def get_all_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    print('userid is: ', session.get('user_id'))
    return jsonify(books or {"message": "Books not found"})

# @book_bp.route('/add_book/', methods=['GET'])
# def get_all_books():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM books")
#     books = cursor.fetchone()
#     return jsonify(books or {"message": "Books not found"})