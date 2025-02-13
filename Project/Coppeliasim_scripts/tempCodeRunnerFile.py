# coppeliasim.py

import sim

# -----------------------------------------------------------------------------
# Define missing constants if they are not present in the sim module.
if not hasattr(sim, 'sim_scripttype_childscript'):
    sim.sim_scripttype_childscript = 0
# -----------------------------------------------------------------------------

def connect_to_coppeliasim(ip='127.0.0.1', port=19997, timeout_ms=5000, thread_cycle=5):
    """
    Connects to a running instance of CoppeliaSim via the Remote API.
    Returns the clientID if successful, or None on failure.
    """
    # Close any previous connections
    sim.simxFinish(-1)
    clientID = sim.simxStart(ip, port, True, True, timeout_ms, thread_cycle)
    
    if clientID == -1:
        print("❌ Error: Could not connect to CoppeliaSim.")
        return None
    print("✅ Connected to CoppeliaSim successfully!")
    return clientID

def load_scene(clientID, scene_path):
    """
    Loads a scene file into CoppeliaSim.
    'scene_path' should be an absolute path using forward slashes.
    """
    scene_path = scene_path.replace("\\", "/")
    ret = sim.simxLoadScene(clientID, scene_path, 0, sim.simx_opmode_blocking)
    
    if ret != 0:
        print("❌ Failed to load scene:", scene_path)
    else:
        print("✅ Scene loaded successfully:", scene_path)
    return ret

def call_script_function(clientID, target_object, function_name,
                         inInts=None, inFloats=None, inStrings=None, inBuffer=b""):
    """
    Calls a function defined in a child script in CoppeliaSim.
    """
    if inInts is None:
        inInts = []
    if inFloats is None:
        inFloats = []
    if inStrings is None:
        inStrings = []
        
    err, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(
        clientID,
        target_object,
        sim.sim_scripttype_childscript,
        function_name,
        inInts,
        inFloats,
        inStrings,
        inBuffer,
        sim.simx_opmode_blocking
    )
    return err, retInts, retFloats, retStrings, retBuffer

def execute_task(clientID, target_object, task_name, paramsFloats=None, paramsStrings=None):
    """
    Executes a high-level task (e.g., "stacking", "moveEndEffector", "rotateJoints")
    as defined in your Lua function 'executeTask'. Optional parameters can be passed:
      - paramsFloats: a list of numeric parameters (e.g., target position for moveEndEffector)
      - paramsStrings: a list of string parameters (if needed)
      
    The task name is sent as the first string.
    """
    if paramsFloats is None:
        paramsFloats = []
    if paramsStrings is None:
        paramsStrings = []
        
    # Combine task name with any additional string parameters.
    allStrings = [task_name] + paramsStrings

    err, retInts, retFloats, retStrings, retBuffer = call_script_function(
        clientID,
        target_object,
        "executeTask",
        inInts=[],           # No integer parameters in this example
        inFloats=paramsFloats,
        inStrings=allStrings,
        inBuffer=b""
    )
    if err == 0:
        print(f"✅ Task '{task_name}' executed successfully.")
    else:
        print(f"❌ Failed to execute task '{task_name}', error code: {err}")
    return err, retInts, retFloats, retStrings, retBuffer

def stack_objects(clientID, target_object):
    """
    Wrapper for executing the stacking task.
    """
    return execute_task(clientID, target_object, "stacking")

# def move_end_effector(clientID, target_object, target_pos):
#     """
#     Wrapper for moving the end effector.
#     'target_pos' should be a list of three floats [x, y, z].
#     """
#     # Pass target_pos as floats; no extra string parameters are needed.
#     return execute_task(clientID, target_object, "moveEndEffector", paramsFloats=target_pos)

# def rotate_joints(clientID, target_object, angles):
#     """
#     (Optional) Wrapper for rotating joints.
#     'angles' should be a list of floats representing the target joint angles.
#     """
#     return execute_task(clientID, target_object, "rotateJoints", paramsFloats=angles)

# -----------------------------------------------------------------------------
# Standalone testing (optional)
def main():
    """
    Main entry point for testing.
    Steps to run in Visual Studio Code:
      1. Save this file as 'coppeliasim.py' in your workspace.
      2. Ensure that the CoppeliaSim remote API library (sim.py) is in your workspace or PYTHONPATH.
      3. Start CoppeliaSim, load your scene (e.g., 'sto.ttt'), and ensure that your target object
         (e.g., "UR5_connection") has a child script with the executeTask function.
      4. Run this file using VS Code (F5) or the integrated terminal:
             python coppeliasim.py
    """
    clientID = connect_to_coppeliasim()
    if clientID is None:
        return

    # Update the scene path to match your system
    scene_path = "C:/Users/DHANASHRI/Downloads/interactive/Coppeliasim_scripts/sto.ttt"
    load_scene(clientID, scene_path)
    
    # Define the target object name that has the child script.
    # This must match exactly what you have in your scene.
    target_object = "UR5_connection"
    
    # Test stacking task
    stack_objects(clientID, target_object)
    
    # Test moving the end effector to a new position, for example [0.5, 0.5, 0.5]
    # move_end_effector(clientID, target_object, [0.5, 0.5, 0.5])
    
    # (Optional) Test rotating joints, if your Lua function is implemented.
    # rotate_joints(clientID, target_object, [30.0, 45.0, 60.0, 0.0, 0.0, 0.0])  # angles in degrees, for example

if __name__ == '__main__':
    main()
