import requests

API_URL = "http://127.0.0.1:5001/send-command"  # Ensure this matches your flask_server.py

def send_command(action, data=None):
    """Send a control command to the Flask server."""
    payload = {"action": action, "data": data or {}}
    
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print("✅ Robot Response:", response.json())
        else:
            print("❌ Error:", response.text)
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")

def main():
    print("\n🤖 Robot CLI Control System")
    print("Commands: start, stop, reset, move_joint, grip, exit\n")
    
    while True:
        command = input("Enter command for the robot: ").strip().lower()
        
        if command == "exit":
            print("👋 Exiting CLI.")
            break
        elif command == "start":
            send_command("start_simulation")
        elif command == "stop":
            send_command("stop_simulation")
        elif command == "reset":
            send_command("reset_position")
        elif command == "move_joint":
            joint = input("Enter joint name (e.g., ur5/joint1): ").strip()
            angle = input("Enter target angle in degrees: ").strip()
            try:
                angle = float(angle)
                send_command("move_joint", {"joint": joint, "angle": angle})
            except ValueError:
                print("❌ Invalid angle. Please enter a number.")
        elif command == "grip":
            state = input("Enter grip state (open/close): ").strip().lower()
            if state in ["open", "close"]:
                send_command("grip", {"state": state})
            else:
                print("❌ Invalid grip state. Use 'open' or 'close'.")
        else:
            print("❌ Invalid command. Use: start, stop, reset, move_joint, grip, exit.")

if __name__ == "__main__":
    main()
