from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# This is a dummy API key, which will be stored in a Kubernetes Secret later.
API_KEY = os.getenv("API_KEY")

@app.route('/pay', methods=['POST'])
def process_payment():
    """Endpoint to simulate processing a payment."""
    payment_data = request.json
    amount = payment_data.get('amount')
    api_key_header = request.headers.get('X-API-Key')

    # Validate against the API key from the environment
    if api_key_header != API_KEY:
        return jsonify({"message": "Unauthorized: Invalid API Key"}), 401

    if amount and amount > 0:
        print(f"Payment of ${amount} processed successfully.")
        return jsonify({"message": "Payment successful", "transaction_id": "txn_12345"}), 200
    else:
        print("Payment failed: Invalid amount.")
        return jsonify({"message": "Payment failed", "error": "Invalid amount"}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)