from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import math

# Connect to CoppeliaSim (if running on a different machine, replace 'localhost' with its IP)
client = RemoteAPIClient('localhost', 23000)
sim = client.getObject('sim')

# Retrieve the target object
target = sim.getObject('/Target')

# Start the simulation
sim.startSimulation()

# Get initial target position for the target object
position = sim.getObjectPosition(target, -1)
a = position[0]
b = position[1]
c = position[2]

mu = 0.1

def moveup():
    global c
    c += mu
    sim.setObjectPosition(target, -1, [a, b, c])

def movedown():
    global c
    c -= mu
    sim.setObjectPosition(target, -1, [a, b, c])

def moveleft(): 
    global a
    a -= mu
    sim.setObjectPosition(target, -1, [a, b, c])

def moveright():    
    global a
    a += mu
    sim.setObjectPosition(target, -1, [a, b, c])

def moveforward():  
    global b
    b += mu
    sim.setObjectPosition(target, -1, [a, b, c])

def movebackward():    
    global b
    b -= mu
    sim.setObjectPosition(target, -1, [a, b, c])

def set_target_position(x, y, z):
    sim.setObjectPosition(target, -1, [x, y, z])

def move_joint(joint_name, angle_delta_deg):
    """
    Moves the joint specified by joint_name by angle_delta_deg degrees.
    The function reads the current joint position, adds the delta, and sets the new position.
    """
    joint_handle = sim.getObject(joint_name)
    if joint_handle is None:
        print(f"Joint {joint_name} not found!")
        return
    # Get current joint position (in radians)
    current_angle = sim.getJointPosition(joint_handle)
    # Compute new target position (convert delta degrees to radians)
    new_angle = current_angle + math.radians(angle_delta_deg)
    sim.setJointTargetPosition(joint_handle, new_angle)
    print(f"Joint {joint_name} moved by {angle_delta_deg}° (new angle: {new_angle:.2f} rad).")

# --- Main Loop with Dynamic Joint and Angle Option ---
while True:
    print("\nChoose an action:")
    print("1. Move Up (target object)")
    print("2. Move Down (target object)")
    print("3. Move Left (target object)")
    print("4. Move Right (target object)")
    print("5. Set Target Position (object)")
    print("6. Move Forward (target object)")
    print("7. Move Backward (target object)")
    print("8. Exit")
    print("9. Move Joint 1 Up by 30° (fixed example)")
    print("10. Specify Joint and Angle")  # New Option

    choice = input("Enter your choice: ")

    if choice == '1':
        moveup()
        print("Moved Up")
    elif choice == '2':
        movedown()
        print("Moved Down")
    elif choice == '3':
        moveleft()
        print("Moved Left")
    elif choice == '4':
        moveright()
        print("Moved Right")
    elif choice == '5':
        x = float(input("Enter X coordinate: "))
        y = float(input("Enter Y coordinate: "))
        z = float(input("Enter Z coordinate: "))
        set_target_position(x, y, z)
        print("Target position set")
    elif choice == '6':
        moveforward()
        print("Moved Forward")
    elif choice == '7':
        movebackward()
        print("Moved Backward")
    elif choice == '8':
        sim.stopSimulation()
        print("Exiting...")
        break
    elif choice == '9':
        # Fixed example: move joint1 by 30°
        move_joint("joint1", 30)
    elif choice == '10':
        # Dynamic option: user specifies the joint and the angle delta
        joint_id = input("Enter joint number (e.g., 1 for 'joint1'): ").strip()
        try:
            angle_delta = float(input("Enter angle delta in degrees (e.g., 30): ").strip())
        except ValueError:
            print("Invalid angle input.")
            continue
        joint_name = f"joint{joint_id}"  # Assuming naming convention "joint1", "joint2", etc.
        move_joint(joint_name, angle_delta)
    else:
        print("Invalid choice. Please try again.")
