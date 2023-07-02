"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""
from utils.creator import *
from utils.logger import enable_logging, log
from PyCloudSim import PyCloudSim




if __name__ == '__main__':
    vm_file = 'csv/vms_test.csv'
    log_file = vm_file.replace('csv', 'log')
    enable_logging(log_file)
    log('INFO', 0, f'Initializing PyCloudSim...')

    # 1) Create Datacenter(s) and Cloud
    datacenters = create_datacenter()
    cloud = create_cloud(datacenters)

    # 2) Create VM(s) either manually or from a file
    vms = create_vms()
    # vms = create_vms()

    # 3) Create a Broker and submit VMs to it
    broker = create_broker(cloud)
    broker.submit_vm_list(vms)
    cloud.set_broker(broker)

    # 4) Create and initialize simulation environment and event processors
    sim_time = 10000
    sim = PyCloudSim(sim_time, broker, cloud, vms)

    # 5) Start the simulation
    sim.start_simulation()

    # 5) Stop the simulation and finalize Results
    sim.stop_simulation()
