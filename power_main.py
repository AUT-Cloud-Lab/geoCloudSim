"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

import logging
from Config import Config as conf
from csv import DictReader, reader
from utils.logger import enable_logging, log
from utils.parser import parse
from utils.plotter import plot_results
from PyCloudSim import PyCloudSim
from utils.creator import *


if __name__ == '__main__':
    if conf.enable_log:
        enable_logging(conf.vm_file.replace('csv', 'log'))
        log('INFO', 0, f'Initializing PyCloudSim...')

    # 1) Create Datacenter(s) and Cloud
    datacenters = create_power_datacenter_from_file(conf.dc_file, conf.pue_file, conf.br_cost_file, conf.solar_file)
    cloud = create_cloud(datacenters)

    # 2) Create VM(s) either manually or from a file
    vms = create_vms(conf.vm_file)
    # vms = create_vms()

    # 3) Create a Broker and submit VMs to it
    broker = create_broker(cloud)
    broker.submit_vm_list(vms)
    cloud.set_broker(broker)

    # 4) Create and initialize simulation environment and event processors
    sim_time = conf.sim_time
    sim = PyCloudSim(sim_time, broker, cloud, vms)

    # 5) Start the simulation
    sim.start_simulation()

    # 5) Stop the simulation and finalize Results
    sim.stop_simulation()

    # 6) Plot the results
    power_readings, num_vms, num_rejected, _ = parse(conf.vm_file.replace('csv', 'log'))
    plot_results(power_readings, num_vms, num_rejected)
