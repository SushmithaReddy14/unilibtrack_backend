from flask import Blueprint, jsonify, request, session
from db_config import get_db_connection

loan_bp = Blueprint('loan_bp', __name__)

@loan_bp.route('/get_loans', methods=['GET'])
def get_loans():
    print("get Loan userid: ", session['user_id'])
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM loans WHERE user_id=%s", (user_id,))
    loan = cursor.fetchall()
    return jsonify(loan or {"message": "loans not found"})


@loan_bp.route('/add_loan', methods=['POST'])
def add_loan():
     if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401
     
     data = request.get_json()
     user_id = data['user_id']
     book_id = data['book_id']
     conn = get_db_connection()
     cursor = conn.cursor(dictionary=True)

     cursor.execute("SELECT title FROM books WHERE book_id = %s", (book_id,))
     book = cursor.fetchone()
     book_title = book['title']

     cursor.execute("""
            INSERT INTO Loans (user_id, book_id, due_date, book_title)
            VALUES (%s, %s, DATE_ADD(CURRENT_DATE(), INTERVAL 14 DAY), %s)
        """, (user_id, book_id, book_title))
     
     cursor.execute("""
            UPDATE reservations SET status = 'Issued'
            WHERE user_id = %s AND book_id = %s
        """, (user_id, book_id))

     cursor.execute("""
            UPDATE Books SET available_copies = available_copies - 1
            WHERE book_id = %s AND available_copies > 0
        """, (book_id,))
     conn.commit()
     conn.close()
     return jsonify({"message": "Book issued successfully"})


@loan_bp.route('/return_book', methods=['PUT'])
def return_book():
    data = request.get_json()
    user_id = data['user_id']
    book_id = data['book_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Loans
        SET return_date = CURRENT_DATE(),
            fine = CASE
                        WHEN CURRENT_DATE() > due_date THEN DATEDIFF(CURRENT_DATE(), due_date) * 1.00
                        ELSE 0
                  END
        WHERE user_id = %s AND book_id = %s
    """, (user_id, book_id))

    cursor.execute("""
            UPDATE reservations SET status = 'Fullfilled'
            WHERE user_id = %s AND book_id = %s
        """, (user_id, book_id))

    # Update available copies
    cursor.execute("""
        UPDATE Books
        SET available_copies = available_copies + 1
        WHERE book_id =  %s
    """, (book_id,))

    conn.commit()
    conn.close()
    return jsonify({"message": "Book returned and fine updated"})
