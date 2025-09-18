from flask import Flask, request, jsonify

app = Flask(__name__)

# This is a dummy API key, which will be stored in a Kubernetes Secret later.
API_KEY = "dummy-api-key-12345"

# Test JSON command: Invoke-RestMethod -Uri http://localhost:5005/pay 
# -Method Post -ContentType "application/json" 
# -Headers @{"X-API-Key"="dummy-api-key-12345"} -Body '{"amount": 25.50}'
@app.route('/pay', methods=['POST'])
def process_payment():
    """Endpoint to simulate processing a payment."""
    payment_data = request.json
    amount = payment_data.get('amount')
    api_key = request.headers.get('X-API-Key')
    
    # Simple validation using the dummy API key.
    if api_key != API_KEY:
        return jsonify({"message": "Unauthorized: Invalid API Key"}), 401

    if amount and amount > 0:
        print(f"Payment of ${amount} processed successfully.")
        return jsonify({"message": "Payment successful", "transaction_id": "txn_12345"}), 200
    else:
        print("Payment failed: Invalid amount.")
        return jsonify({"message": "Payment failed", "error": "Invalid amount"}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return "OK", 200

if __name__ == '__main__':
    # Run the Flask app on all available network interfaces.
    app.run(host='0.0.0.0', port=5005)