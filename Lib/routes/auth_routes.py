from flask import Blueprint, jsonify, request, session
from db_config import get_db_connection

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM users
        WHERE email = %s AND password = %s
    """, (username, password))
    user = cursor.fetchone()
    conn.close()
    print("userID: ", user['user_id'], "name: ", user['name'] )
    if user:
        session['user_id'] = user['user_id']
        session['email'] = user['email']
        session['username'] = user['name']
        print("Session retrieved:", session['user_id'])
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
# Register User
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstName = data['firstName']
    lastName = data['lastName']
    name = firstName + " " + lastName
    email = data['email']
    password = data['password']
    userType = data['userType']
    department = data['department']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
            INSERT INTO users (first_name, last_name, name, email, password, department, user_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (firstName, lastName, name, email, password, department, userType))
    conn.commit()

    if cursor.rowcount == 1:
        cursor.execute("""
        SELECT * FROM users
        WHERE email = %s AND password = %s
        """, (email, password))
        user = cursor.fetchone()
        conn.close()
        print("registration userID: ", user['user_id'], "name: ", user['name'] )
        if user:
            session['user_id'] = user['user_id']
            session['email'] = user['email']
            session['username'] = user['name']
            print("Session retrieved:", session['user_id'])

        user = {
            "first_name" : firstName,
            "last_name" : lastName,
            "name" : name,
            "email" : email,
            "user_type" : userType,
            "department" : department
        }
        conn.close()
        return jsonify({"status" : 1,  "message" : "User Registered Successfully", "user": user})
    else :
        conn.close()
        return jsonify({"status" : 2, "message" : "User registration failed"})
    

# Logout route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})