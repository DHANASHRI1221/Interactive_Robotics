sim=require 'sim'
simIK=require 'simIK'

function sysCall_init()
    -- Take a few handles from the scene:
    simBase = sim.getObject('../redundantRobot')
    simTip = sim.getObject('../redundantRobot/tip')
    simTarget = sim.getObject('../redundantRobot/target')
    
    -- Initialize the IK environment
    ikEnv = simIK.createEnvironment()
    
    -- Prepare the 2 ik groups using convenience functions 'simIK.addElementFromScene'
    ikGroup_undamped = simIK.createGroup(ikEnv)
    simIK.setGroupCalculation(ikEnv, ikGroup_undamped, simIK.method_pseudo_inverse, 0, 10)
    simIK.addElementFromScene(ikEnv, ikGroup_undamped, simBase, simTip, simTarget, simIK.constraint_pose)
    
    ikGroup_damped = simIK.createGroup(ikEnv)
    simIK.setGroupCalculation(ikEnv, ikGroup_damped, simIK.method_damped_least_squares, 0.3, 99)
    simIK.addElementFromScene(ikEnv, ikGroup_damped, simBase, simTip, simTarget, simIK.constraint_pose)
end

function sysCall_actuation()
    -- Handle IK group calculations
    if simIK.handleGroup(ikEnv, ikGroup_undamped, {syncWorlds=true}) ~= simIK.result_success then
        simIK.handleGroup(ikEnv, ikGroup_damped, {syncWorlds=true, allowError=true})
    end
end

function sysCall_cleanup()
    -- Cleanup the IK environment
    simIK.eraseEnvironment(ikEnv)
end

function sysCall_sensing()
    -- Print the positions of all 7 joints
    for i = 1, 7 do
        local jointHandle = sim.getObjectHandle('redundantRobot_joint' .. i)
        if jointHandle ~= -1 then
            local position = sim.getJointPosition(jointHandle)
            print("?? Joint " .. i .. " Position: " .. position)
        else
            print("? ERROR: Joint redundantRobot_joint" .. i .. " not found!")
        end
    end
end
