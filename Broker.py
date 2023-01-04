"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulation framework
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

import simpy
from simpy.util import start_delayed
import logging


class Broker:
    """ Broker class definition: It is responsible for managing VMs (creation, submission, destruction) on behalf of
    users
    :ivar _sim_time: simulation time
    :type _sim_time: int
    :ivar _env: simulation environment
    :type _env: simpy env
    :ivar _vm_list: list of VMs
    :type _vm_list: list[VM]
    :ivar _vms_created_list: list of created VMs
    :type _vms_created_list: list[VM]
    :ivar _vms_requested: number of VM creation requests
    :type _vms_requested: int
    :ivar _vms_acks: number of VM creation request acknowledgement
    :type _vms_acks: int
    :ivar _vms_destroyed: number of VM destroyed
    :type _vms_destroyed: int
    :ivar _datacenter_list: list of datacenters
    :type _datacenter_list: list[Datacenter]
    :ivar _datacenter_requested_ids_list: list of ids of requested datacenters
    :type _datacenter_requested_ids_list: list[int]
    :ivar _vms_datacenter_map: mapping of VMs to datacenters
    :type _vms_datacenter_map: dict<VM, Datacenter>
    :ivar _cloud: the cloud instance that includes all datacenters
    :type _cloud: Cloud
    """
    def __init__(self, cloud):
        self._sim_time = None
        self._env = None
        self._vm_list = []
        self._vms_created_list = []
        self._vms_requested = 0
        self._vms_acks = 0
        self._vms_destroyed = 0
        self._datacenter_list = cloud.get_dc_list()
        self._datacenter_requested_ids_list = []
        self._vms_datacenter_map = dict()
        self._cloud = cloud
        # self._datacenter_characteristics_map = dict()

    def submit_vm_list(self, vm_list):
        [self._vm_list.append(vm) for vm in vm_list]

    def start_run(self, env, sim_time):
        self._env = env
        self._sim_time = sim_time
        logging.info(f'Broker started at {env.now}.')
        dc = self._datacenter_list[0]
        for vm in self._vm_list:
            vm_delay = vm.get_arrival_time() - env.now
            request = {'dest': 'datacenter', 'type': 'vm_create', 'vm': vm, 'dc': dc}
            if vm_delay == 0:
                yield env.process(self.send_request(env, request))
            else:
                yield start_delayed(env, self.send_request(env, request), delay=vm_delay)
        logging.info(f'Broker stopped at {env.now}.')

    def send_request(self, env, request):
        if request['type'] == 'vm_create':
            dc = request['dc']
            vm = request['vm']
            logging.info(f'VM request with vm_id = {vm.get_id()} sent at {env.now}.')
            yield env.process(dc.process_vm_create(env, vm))
            logging.info(f'VM request with vm_id = {vm.get_id()} completed at {env.now}.')

    def run(self):
        while True:
            try:
                yield self._env.timeout(self._sim_time - self._env.now)
            except simpy.Interrupt:
                print('What?!')

    def process_event(self, event):
        pass
