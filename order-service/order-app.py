import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
orders = {}
order_id_counter = 1

@app.route('/order', methods=['POST'])
def place_order():
    global order_id_counter
    order_details = request.json
    
    # 1. Validate with Menu Service
    try:
        menu_response = requests.get('http://menu-service:5006/menu')
        menu_items = menu_response.json()
        # Add your validation logic here (ex, check if order_details.items exist in menu_items)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to menu-service: {e}"}), 503

    # 2. Process payment with Payment Service
    try:
        payment_payload = {"amount": 25.50} # Dummy amount
        headers = {"X-API-Key": "dummy-api-key-12345"} # Hardcoded for now
        payment_response = requests.post('http://payment-service:5005/pay', json=payment_payload, headers=headers)
        if payment_response.status_code != 200:
            return jsonify({"error": "Payment failed"}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to payment-service: {e}"}), 503

    # Assign a unique ID and store the order
    order_id = order_id_counter
    orders[order_id] = {
        "status": "received",
        "details": order_details
    }
    order_id_counter += 1

    # 3. Trigger cooking with Kitchen Service
    try:
        kitchen_response = requests.post(f'http://kitchen-service:5002/cook/{order_id}')
        if kitchen_response.status_code != 200:
            # Handle the case where the kitchen service failed to start cooking
            pass
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to kitchen-service: {e}"}), 503

    print(f"New order placed: ID {order_id}")
    return jsonify({"message": "Order received", "order_id": order_id}), 201

@app.route('/order/<int:order_id>', methods=['GET'])
def get_order_status(order_id):
    """Endpoint to check the status of a specific order."""
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return "OK", 200

if __name__ == '__main__':
    # Run the Flask app on all available network interfaces
    app.run(host='0.0.0.0', port=5001)