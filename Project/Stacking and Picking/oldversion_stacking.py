from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')

target = sim.getObject('/Target')
# Start the simulation
sim.startSimulation()
sim.coroutineMain()
