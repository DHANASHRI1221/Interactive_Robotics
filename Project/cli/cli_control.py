import requests

API_URL = "http://127.0.0.1:5000/send-command"

def send_command(command):
    """Send a control command to the Flask server."""
    response = requests.post(API_URL, json={"command": command})
    if response.status_code == 200:
        print("✅ Robot Response:", response.json())
    else:
        print("❌ Error:", response.text)

def main():
    print("\n🤖 Robot CLI Control System")
    print("Commands: move_joint, grip, stacking, exit\n")
    
    while True:
        command = input("Enter command for the robot: ").strip().lower()
        
        # Check for exit command
        if command == "exit":
            print("👋 Exiting CLI.")
            break
        
        # Handle invalid commands or empty input
        if command not in ["move_joint", "grip", "stacking"]:
            print("❌ Invalid command. Please enter a valid command from: move_joint, grip, stacking.")
            continue
        
        # Send valid command to Flask server
        send_command(command)

if __name__ == "__main__":
    main()
