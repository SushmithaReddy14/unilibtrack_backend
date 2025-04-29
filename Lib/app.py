from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_mysqldb import MySQL

from routes.user_routes import user_bp
from routes.book_routes import book_bp
from routes.loan_routes import loan_bp
from routes.reservation_routes import reservation_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.secret_key = 'ff#%455hjbk'

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

CORS(app, supports_credentials=True, origins=[
    "https://unilibtrack-frontend.onrender.com",
    "http://localhost:3000"
])

app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(book_bp, url_prefix="/books")
app.register_blueprint(loan_bp, url_prefix="/loans")
app.register_blueprint(reservation_bp, url_prefix = "/reservations")
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return "API is working now...!!!"

if __name__ == '__main__':
    app.run(debug=True)
