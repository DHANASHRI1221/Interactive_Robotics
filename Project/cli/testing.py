import websocket
import json
import threading

# WebSocket server address (CoppeliaSim should be running)
WS_HOST = "ws://127.0.0.1:23050"

def on_message(ws, message):
    """Handles messages from the server."""
    print(f"Received: {message}")

def on_error(ws, error):
    """Handles errors."""
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Handles closing the connection."""
    print("WebSocket connection closed")

def on_open(ws):
    """Sends initial command when connected."""
    print("Connected to WebSocket server")

    # Start simulation
    ws.send(json.dumps({
        "function": "simxStartSimulation",
        "params": []
    }))
    print("Simulation started")

def send_target_position(ws, x, y, z):
    """Sends target end-effector position for IK control."""
    data = {
        "function": "move_target",
        "params": [x, y, z]
    }
    ws.send(json.dumps(data))
    print(f"Sent target position: X={x}, Y={y}, Z={z}")

def user_input_loop(ws):
    """Handles user input."""
    while True:
        try:
            cmd = input("Enter target X Y Z (or 'exit' to quit): ")
            if cmd.lower() == "exit":
                ws.close()
                break
            
            # Parse input
            x, y, z = map(float, cmd.split())
            send_target_position(ws, x, y, z)
        except Exception as e:
            print(f"Invalid input: {e}")

# Start WebSocket client
ws = websocket.WebSocketApp(WS_HOST, on_message=on_message, on_error=on_error, on_close=on_close)
ws.on_open = on_open

# Run WebSocket in a separate thread
ws_thread = threading.Thread(target=ws.run_forever, daemon=True)
ws_thread.start()

# Start user input loop
user_input_loop(ws)
