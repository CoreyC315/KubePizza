from flask import Flask, jsonify

app = Flask(__name__)

# A hardcoded list of pizzas for the menu. Could change to something else for easy changing
pizzas = [
    {"id": 1, "name": "Margherita", "toppings": ["tomato", "mozzarella", "basil"]},
    {"id": 2, "name": "Pepperoni", "toppings": ["tomato", "mozzarella", "pepperoni"]},
    {"id": 3, "name": "Hawaiian", "toppings": ["tomato", "mozzarella", "ham", "pineapple"]},
]

@app.route('/menu', methods=['GET'])
def get_menu():
    """Returns the list of pizzas on the menu."""
    return jsonify(pizzas)

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return "OK", 200

if __name__ == '__main__':
    # Run the Flask App on all available network interfaces
    app.run(host='0.0.0.0', port=5006)