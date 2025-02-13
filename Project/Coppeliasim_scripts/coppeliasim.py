# coppeliasim.py

import sim
import time

# Define missing constants if they are not present in the sim module.
if not hasattr(sim, 'sim_scripttype_childscript'):
    sim.sim_scripttype_childscript = 0

def connect_to_coppeliasim(ip='127.0.0.1', port=19997, timeout_ms=5000, thread_cycle=5):
    """
    Connect to a running instance of CoppeliaSim via the Remote API.
    Returns the clientID if successful, or None on failure.
    """
    sim.simxFinish(-1)  # Close any previous connections
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
    Executes a task by calling the 'executeTask' function in the Lua child script.
    """
    if paramsFloats is None:
        paramsFloats = []
    if paramsStrings is None:
        paramsStrings = []
        
    # Combine the task name with any additional string parameters.
    allStrings = [task_name] + paramsStrings

    err, retInts, retFloats, retStrings, retBuffer = call_script_function(
        clientID,
        target_object,
        "executeTask",
        inInts=[],           # no integer parameters
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

def main():
    """
    Main entry point for testing:
      1. Connect to CoppeliaSim.
      2. Load the scene.
      3. Execute the stacking task.
    """
    clientID = connect_to_coppeliasim()
    if clientID is None:
        return

    # Update the scene path to match your system:
    scene_path = "C:/Users/DHANASHRI/Downloads/interactive/Coppeliasim_scripts/sto.ttt"
    load_scene(clientID, scene_path)
    
    # Define the target object name that has the child script (must match exactly, e.g., "UR5")
    target_object = "UR5"
    
    # Wait a moment for the scene to load completely
    time.sleep(2)
    
    # Execute the stacking task
    stack_objects(clientID, target_object)
    
    # Optionally, wait a moment then close the connection
    time.sleep(2)
    sim.simxFinish(clientID)
    print("Connection closed.")

if __name__ == '__main__':
    main()
