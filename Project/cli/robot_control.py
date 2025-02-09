import websocket
import json

ws = websocket.WebSocket()
ws.connect("ws://localhost:23050")

test_command = {
    "function": "move_target",
    "params": [0.3, 0.2, 0.5]  # X, Y, Z
}

print("📤 Sending test command to CoppeliaSim...")
ws.send(json.dumps(test_command))

response = ws.recv()
print(f"📩 Response from CoppeliaSim: {response}")

ws.close()
