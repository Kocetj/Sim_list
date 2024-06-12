import os
import subprocess


sumo_path = r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo-gui.exe"
sumo_config = "sim_list.sumo.cfg"

sumo_cmd = [sumo_path, "-c", sumo_config, "--start"]

subprocess.Popen(sumo_cmd)
