# from flask import Flask, render_template, request, jsonify
# import socket  # For socket communication with CoppeliaSim

# app = Flask(__name__)

# # Replace with the IP and port of the CoppeliaSim remote API server
# COPPELIA_SIM_IP = '127.0.0.1'
# COPPELIA_SIM_PORT = 19997

# def send_to_coppeliasim(data):
#     """Send data to the CoppeliaSim remote API server via sockets."""
#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((COPPELIA_SIM_IP, COPPELIA_SIM_PORT))
#             s.sendall(data.encode())
#             response = s.recv(1024).decode()
#             return response
#     except Exception as e:
#         return str(e)

# @app.route('/')
# def home():
#     return render_template('gui.html')

# @app.route('/send-command', methods=['POST'])
# def send_command():
#     data = request.json
#     action = data.get('action')
#     command_data = data.get('data')

#     # Log the received data
#     print(f"Received action: {action}")
#     print(f"Received data: {command_data}")

#     # Prepare the command to send to CoppeliaSim
#     if action == 'move_joint':
#         joint = command_data.get('joint')
#         angle = command_data.get('angle')
#         command = f"move_joint {joint} {angle}"
#     elif action == 'move_effector':
#         x = command_data.get('x')
#         y = command_data.get('y')
#         z = command_data.get('z')
#         command = f"move_effector {x} {y} {z}"
#     elif action == 'pick_object':
#         command = "pick_object"
#     elif action == 'stack_objects':
#         command = "stack_objects"
#     else:
#         return jsonify({"message": "Invalid action"}), 400

#     # Send command to CoppeliaSim
#     response = send_to_coppeliasim(command)
#     return jsonify({"message": response})

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)


from flask import Flask, render_template, request, jsonify
import requests  # Use this to communicate with backend (flask_server.py)

app = Flask(__name__)

# Backend API (Flask server handling CoppeliaSim)
BACKEND_URL = "http://127.0.0.1:5001/send-command"

@app.route('/')
def home():
    return render_template('gui.html')



@app.route('/send-command', methods=['POST'])



def send_command():
    data = request.json
    action = data.get('action')
    command_data = data.get('data', {})

    if action == 'move_up':
        command = "move_up"
    elif action == 'move_down':
        command = "move_down"
    elif action == 'move_left':
        command = "move_left"
    elif action == 'move_right':
        command = "move_right"
    elif action == 'move_forward':
        command = "move_forward"
    elif action == 'move_backward':
        command = "move_backward"
    elif action == 'move_backward':
        command = "move_backward"
    elif action == 'start_simulation':
        command = "start_simulation"  
    elif action == 'stop_simulation':
        command = "stop_simulation"  
    elif action == 'reset_position':
        command = "reset_position"      
    elif action == 'set_target_position':
        x = command_data.get('x')
        y = command_data.get('y')
        z = command_data.get('z')
        command = f"set_target_position {x} {y} {z}"
    elif action == 'move_joint':
        joint = command_data.get('joint')
        angle = command_data.get('angle')
        command = f"move_joint {joint} {angle}"
    else:
        return jsonify({"message": "Invalid action"}), 400

    # Send command to backend
    response = send_command(command)
    return jsonify({"message": response})

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # GUI runs on port 5002
