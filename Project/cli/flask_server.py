from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask server is running!"})

@app.route('/send-command', methods=['POST'])
def send_command():
    data = request.get_json()  # Ensure JSON is parsed
    if not data or "command" not in data:
        return jsonify({"error": "No command received"}), 400

    command = data["command"]
    
    # Simulated response (Replace with actual logic)
    response = {"status": "success", "command_executed": command}
    
    return jsonify(response)

if __name__ == '__main__':
    print("Starting Flask server at http://127.0.0.1:5000/")
    app.run(host='127.0.0.1', port=5000, debug=True)

