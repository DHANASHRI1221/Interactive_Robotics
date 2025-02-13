from flask import Flask, render_template, request, jsonify
import socket  # For socket communication with CoppeliaSim

app = Flask(__name__)

# Replace with the IP and port of the CoppeliaSim remote API server
COPPELIA_SIM_IP = '127.0.0.1'
COPPELIA_SIM_PORT = 19997

def send_to_coppeliasim(data):
    """Send data to the CoppeliaSim remote API server via sockets."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((COPPELIA_SIM_IP, COPPELIA_SIM_PORT))
            s.sendall(data.encode())
            response = s.recv(1024).decode()
            return response
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template('gui.html')

@app.route('/send-command', methods=['POST'])
def send_command():
    data = request.json
    action = data.get('action')
    command_data = data.get('data')

    # Log the received data
    print(f"Received action: {action}")
    print(f"Received data: {command_data}")

    # Prepare the command to send to CoppeliaSim
    if action == 'move_joint':
        joint = command_data.get('joint')
        angle = command_data.get('angle')
        command = f"move_joint {joint} {angle}"
    elif action == 'move_effector':
        x = command_data.get('x')
        y = command_data.get('y')
        z = command_data.get('z')
        command = f"move_effector {x} {y} {z}"
    elif action == 'pick_object':
        command = "pick_object"
    elif action == 'stack_objects':
        command = "stack_objects"
    else:
        return jsonify({"message": "Invalid action"}), 400

    # Send command to CoppeliaSim
    response = send_to_coppeliasim(command)
    return jsonify({"message": response})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
