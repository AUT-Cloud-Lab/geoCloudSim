"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

import simpy
import logging

from utils.logger import log


class PyCloudSim(object):
    """
    PyCloudSim class definition: It is responsible for initializing, starting and stopping the simulator
    :ivar _sim_time: simulation time
    :type _sim_time: int
    :ivar _env: simulation environment
    :type _env: simpy env
    :ivar _vm_list: list of VMs that to be processed
    :type _vm_list: list[VM]
    :ivar _cloud: an instance of Cloud class
    :type _cloud: Cloud
    :ivar _broker: an instance of Broker
    :type _broker: Broker
    """

    def __init__(self, sim_time, broker, cloud, vm_list):
        log('INFO', 0, f'Creating PyCloudSim environment.')
        if isinstance(sim_time, int) and sim_time > 0:
            self._sim_time = sim_time
        else:
            raise ValueError('The value should be a positive integer.')
        self._env = simpy.Environment()
        self._broker = broker
        self._cloud = cloud
        self._datacenter_list = cloud.get_dc_list()
        self._vm_list = vm_list
        self._env.process(self._broker.start_run(self._env, sim_time))
        [self._env.process(dc.start_run(self._env, sim_time)) for dc in self._datacenter_list]
        self._env.process(self._cloud.start_run(self._env, sim_time))

    def get_sim_time(self):
        return self._sim_time

    def _set_sim_time(self, sim_time):
        self._sim_time = sim_time

    def get_env(self):
        return self._env

    def _set_env(self, env):
        self._env = env

    def start_simulation(self):
        log('INFO', 0, f'Starting simulation.')
        self.get_env().run(until=self.get_sim_time())

    def stop_simulation(self):
        log('INFO', int(self._env.now), 'Simulation Finished.')
        cost = [dc.get_brown_cost() for dc in self._datacenter_list if callable(getattr(dc, 'get_brown_cost', None))]
        log('STAT', int(self._env.now), f'Total cost of all datacenters = {sum(cost)}')


