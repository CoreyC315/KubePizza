from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Define the path to the mounted ConfigMap file
MENU_FILE_PATH = "/app/config/menu.json"

def load_menu():
    """Loads the menu data from the JSON file."""
    try:
        with open(MENU_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Menu file not found at {MENU_FILE_PATH}")
        return {"pizzas": [], "specials": []}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in menu file at {MENU_FILE_PATH}")
        return {"pizzas": [], "specials": []}

@app.route('/menu', methods=['GET'])
def get_menu():
    """Returns the menu loaded from the ConfigMap."""
    menu_data = load_menu()
    return jsonify(menu_data.get("pizzas", []))

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return "OK", 200

if __name__ == '__main__':
    # The application will now use the menu data from the mounted file
    app.run(host='0.0.0.0', port=5006)