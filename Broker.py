"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

import simpy
from simpy.util import start_delayed
import logging


class Broker:
    """ Broker class definition: It is responsible for sending VMs request (creation, submission, destruction) to Cloud
    on behalf of users.
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
        """ Constructor
        :param cloud: the cloud instance that includes all datacenters
        """
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
        """ Submit the list of VMs to the broker
        :param vm_list: list of VMs
        """
        [self._vm_list.append(vm) for vm in vm_list]

    def start_run(self, env, sim_time):
        """Start the broker event processor
        :param env: the simulation environment
        :param sim_time: the simulation duration
        """
        self._env = env
        self._sim_time = sim_time
        logging.info(f'Broker started at {env.now}.')
        dc = self._datacenter_list[0]
        for vm in self._vm_list:
            vm_delay = vm.get_arrival_time() - env.now
            request = {'dest': 'cloud', 'type': 'vm_create', 'vm': vm}
            if vm_delay == 0:
                yield env.process(self.send_request(request))
            else:
                yield start_delayed(env, self.send_request(request), delay=vm_delay)
        logging.info(f'Broker stopped at {env.now}.')

    def send_request(self, request):
        """ Sending request (VM creation, etc.) to Cloud/Datacenters
        :param request:  a dictionary containing the request type, destination, etc.
        """
        if request['type'] == 'vm_create' and request['dest'] == 'cloud':
            vm = request['vm']
            logging.info(f'VM creation request with vm_id = {vm.get_id()} sent to cloud at {self._env.now}.')
            yield self._env.process(self._cloud.process_vm_create(vm))

    def process_ack(self, ack):
        logging.info(ack['message'])

