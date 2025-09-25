import requests
from flask import Flask, request, jsonify
import psycopg2
import json 
import threading 
import os 

app = Flask(__name__)

# Database connection details from environment variables
DB_HOST = "order-db-service"
DB_NAME = "orders"
DB_USER = "user"
DB_PASSWORD = os.getenv("DB_PASSWORD") # <-- Read password from environment

# Function to connect to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def send_to_kitchen_in_background(order_id):
    """
    Sends the order to the Kitchen Service in a separate thread.
    This call is now non-blocking for the user.
    """
    try:
        print(f"Sending order {order_id} to kitchen...")
        kitchen_response = requests.post(f'http://kitchen-service:5002/cook/{order_id}')
        if kitchen_response.status_code != 200:
            print(f"Error sending order {order_id} to kitchen.")
        else:
            print(f"Order {order_id} successfully sent to kitchen.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to kitchen-service for order {order_id}: {e}")

@app.route('/order', methods=['POST'])
def place_order():
    order_details = request.json
    
    # 1. Validate with Menu Service
    try:
        menu_response = requests.get('http://menu-service:5006/menu')
        menu_items = menu_response.json()
        # Add your validation logic here
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to menu-service: {e}"}), 503

    # 2. Process payment with Payment Service
    try:
        # Get the API key from the environment variable
        api_key = os.getenv("API_KEY") 
        if not api_key:
            return jsonify({"error": "API Key not configured"}), 500

        payment_payload = {"amount": 25.50} 
        headers = {"X-API-Key": api_key} # <-- Use the API key from the environment
        payment_response = requests.post('http://payment-service:5005/pay', json=payment_payload, headers=headers)
        if payment_response.status_code != 200:
            return jsonify({"error": "Payment failed"}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to payment-service: {e}"}), 503

    # Store the new order in the database
    order_id = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
        cur = conn.cursor()
        cur.execute("INSERT INTO orders (customer_name, status, details) VALUES (%s, %s, %s) RETURNING id;",
                    (order_details['customer_name'], 'received', json.dumps(order_details)))
        order_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to save order to database: {error}")
        return jsonify({"error": "Failed to save order to database"}), 500

    # Trigger cooking in the background (asynchronous part)
    thread = threading.Thread(target=send_to_kitchen_in_background, args=(order_id,))
    thread.start()

    print(f"New order placed: ID {order_id}. Confirmation sent to user.")
    return jsonify({"message": "Order received and being processed.", "order_id": order_id}), 201

@app.route('/order/<int:order_id>', methods=['GET'])
def get_order_status(order_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cur = conn.cursor()
        cur.execute("SELECT status, details FROM orders WHERE id = %s;", (order_id,))
        order = cur.fetchone()
        cur.close()
        conn.close()
        
        if not order:
            return jsonify({"error": "Order not found"}), 404
            
        status, details = order
        return jsonify({"id": order_id, "status": status, "details": json.loads(details)}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to retrieve order from database: {error}")
        return jsonify({"error": "Failed to retrieve order from database"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)