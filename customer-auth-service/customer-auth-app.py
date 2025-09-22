from flask import Flask, request, jsonify
import os

app = Flask(__name__)

DUMMY_USER_EMAIL = os.getenv("USER_EMAIL")
DUMMY_USER_PASSWORD = os.getenv("USER_PASSWORD")

# A simple dictionary to store user accounts in memory
# In a real app, this would be a database
users = {
    DUMMY_USER_EMAIL: {
        "password": DUMMY_USER_PASSWORD,
        "order_history": ["order_1", "order_2"]
    }
}
tokens = {} # In-memory dictionary for auth tokens

@app.route('/register', methods=['POST'])
def register_user():
    """Endpoint to create a new user account."""
    user_data = request.json
    email = user_data.get('email')
    password = user_data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if email in users:
        return jsonify({"error": "User with this email already exists"}), 409

    users[email] = {
        "password": password,
        "order_history": []
    }
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login_user():
    login_data = request.json
    email = login_data.get('email')
    password = login_data.get('password')

    user = users.get(email)
    if not user or user.get("password") != password:
        return jsonify({"error": "Invalid email or password"}), 401

    auth_token = f"auth_token_for_{email}"
    tokens[auth_token] = email

    return jsonify({"message": "Login successful", "token": auth_token}), 200

@app.route('/orders', methods=['GET'])
def get_order_history():
    """Endpoint to retrieve a user's order history using an auth token."""
    auth_token = request.headers.get('Authorization')
    email = tokens.get(auth_token)

    if not email:
        return jsonify({"error": "Unauthorized"}), 401

    user = users.get(email)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify({"order_history": user.get("order_history")}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)