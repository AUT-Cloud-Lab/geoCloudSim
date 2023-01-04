"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulation framework
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

import simpy
import logging


class PyCloudSim(object):
    """
    This is pyCloudSim class, which is used to initialize, start and stop the simulator
    """

    def __init__(self, sim_time, broker, datacenter_list, vm_list):
        logging.info(f'Creating PyCloudSim environment.')
        if isinstance(sim_time, int) and sim_time > 0:
            self._sim_time = sim_time
        else:
            raise ValueError('The value should be a positive integer.')
        self._env = simpy.Environment()
        self._broker = broker
        self._datacenter_list = datacenter_list
        self._vm_list = vm_list
        self._env.process(self._broker.start_run(self._env, sim_time))

    def get_sim_time(self):
        return self._sim_time

    def _set_sim_time(self, sim_time):
        self._sim_time = sim_time

    def get_env(self):
        return self._env

    def _set_env(self, env):
        self._env = env

    def start_simulation(self):
        logging.info(f'Starting simulation.')
        self.get_env().run(until=self.get_sim_time())

    def stop_simulation(self):
        pass
