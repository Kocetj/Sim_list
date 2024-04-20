import os, sys
import time

import traci
import traci.constants

sumoCmd = ["sumo-gui", "-c", "sim_list.sumocfg", "--start"]
traci.start(sumoCmd)

traci.gui.setSchema("View #0", "real world")

j=0
while (j < 1000):
    traci.simulationStep()
    j+=1


traci.close()
