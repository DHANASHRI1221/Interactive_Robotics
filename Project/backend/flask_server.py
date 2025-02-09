from flask import Flask, request, jsonify
from pyrep import PyRep
from pyrep.robots.arm import Panda  # Using the Panda robotic arm as an example

app = Flask(__name__)

# Path to your CoppeliaSim scene file (.ttt)
SCENE_FILE = "path/to/your/coppeliasim/scene.ttt"

# Initialize the PyRep simulation
pr = PyRep()
pr.launch(SCENE_FILE, headless=False)
pr.start()

# Load the robotic arm (Panda in this case)
robot = Panda()

@app.route('/voice-command', methods=['POST'])
def voice_command():
    data = request.json
    action = data.get("action")
    params = data.get("data")

    if action == "move_joint":
        joint_id = params['joint']
        angle = params['angle']
        robot.set_joint_target_position(joint_id, angle)
        pr.step()  # Advance simulation step
        return jsonify({"status": "success", "message": f"Moved Joint {joint_id} by {angle} degrees"}), 200

    elif action == "pick_object":
        object_name = params['object']
        # Code to pick the object in CoppeliaSim
        return jsonify({"status": "success", "message": f"Picked up {object_name}"}), 200

    elif action == "stack_objects":
        # Code to stack objects in CoppeliaSim
        return jsonify({"status": "success", "message": "Stacked objects"}), 200

    else:
        return jsonify({"status": "error", "message": "Invalid command"}), 400

if __name__ == '__main__':
    app.run(debug=True)

