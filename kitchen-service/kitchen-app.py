from flask import Flask, request, jsonify
import time
import requests

app = Flask(__name__)

# This is a dummy dictionary to simulate a connection to the Order Service.
# In Phase 2, this would be a real network call to the Order Service's API.
order_statuses = {}

@app.route('/cook/<int:order_id>', methods=['POST'])
def cook_order(order_id):
    """Simulates the cooking process for a given order."""
    
    if order_id in order_statuses and order_statuses[order_id]['status'] != 'received':
        return jsonify({"message": f"Order {order_id} is already being handled."}), 409

    print(f"Kitchen Service received order {order_id}. Cooking...")
    
    # Simulate a network call to the Order Service to update the status to 'cooking'.
    # For now, we'll just update a local dictionary.
    order_statuses[order_id] = {'status': 'cooking'}
    
    # Simulate the "cooking" time
    cooking_time = 10  # 10 seconds
    time.sleep(cooking_time)
    
    # After "cooking," update the status to 'ready'.
    order_statuses[order_id]['status'] = 'ready'
    
    print(f"Order {order_id} is ready for delivery!")
    
    # Make an API call to the Delivery Service
    try:
        delivery_response = requests.post(f'http://delivery-service:5003/deliver/{order_id}')
        if delivery_response.status_code == 200:
            print(f"Order {order_id} handed off to Delivery Service successfully.")
        else:
            print(f"Error handing off order {order_id} to Delivery Service.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to delivery-service: {e}")
        
    return jsonify({"message": f"Order {order_id} is ready for delivery!"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return "OK", 200

if __name__ == '__main__':
    # Run the Flask app on all available network interfaces
    app.run(host='0.0.0.0', port=5002)