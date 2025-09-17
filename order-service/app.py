from flask import Flask, request, jsonify

app = Flask(__name__)

# A simple dictionary to store orders in memory
# In a real-world application, this would be a database
orders = {}
order_id_counter = 1

@app.route('/order', methods=['POST'])
def place_order():
    """Endpoint for placing a new pizza order."""
    global order_id_counter
    order_details = request.json
    
    # Simple validation to ensure order data is present
    if not order_details:
        return jsonify({"error": "No order details provided"}), 400

    # Assign a unique ID and store the order
    order_id = order_id_counter
    orders[order_id] = {
        "status": "received",
        "details": order_details
    }
    order_id_counter += 1

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