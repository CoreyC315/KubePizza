from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# This is a dummy dictionary to simulate orders ready for delivery.
delivery_orders = {}

@app.route('/deliver/<int:order_id>', methods=['POST'])
def deliver_order(order_id):
    """Simulates the delivery process for a given order."""
    
    if order_id in delivery_orders and delivery_orders[order_id]['status'] == 'in_transit':
        return jsonify({"message": f"Order {order_id} is already out for delivery."}), 409

    print(f"Delivery Service received order {order_id}. Sending out for delivery...")
    
    # Simulate the "delivery" process.
    delivery_orders[order_id] = {'status': 'in_transit'}

    # Simulate the delivery time
    delivery_time = 15  # 15 seconds
    time.sleep(delivery_time)
    
    # After "delivery," update the status to 'delivered'.
    delivery_orders[order_id]['status'] = 'delivered'
    
    print(f"Order {order_id} has been delivered!")
    
    # In a real-world app, you might make another API call to the Order Service
    # to update the master order record.
    
    return jsonify({"message": f"Order {order_id} has been delivered!"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return "OK", 200

if __name__ == '__main__':
    # Run the Flask app on all available network interfaces.
    app.run(host='0.0.0.0', port=5003)