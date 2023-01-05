"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

import logging


class Cloud:
    """ Cloud class definition: It is responsible for managing datacenter selection for incoming VMs via its
    datacenter selection policy
    :ivar _env: simulation environment
    :type _env: simpy env
    :ivar _sim_time: simulation duration
    :type _sim_time: int
    :ivar _cloud_id: id of this cloud
    :type _cloud_id: int
    :ivar _dc_selection_policy: a policy that determines how datacenters are selected for incoming VMs
    :type _dc_selection_policy: VMAllocationPolicy or its subclasses
    :ivar _last_process_time: ? unused for now
    :type _last_process_time: int
    :ivar _dc_list: list of datacenters in this cloud
    :type _dc_list: list[Datacenter]
    """

    def __init__(self, cloud_attributes, dc_list, dc_selection_policy):
        self._env = None
        self._sim_time = None
        self._cloud_id = cloud_attributes['cloud_id']
        self._dc_selection_policy = dc_selection_policy
        self._last_process_time = 0
        self._dc_list = dc_list
        self._broker = None
        self._dc_tried = 0
        self._vm_create_events = {}
        if not dc_list:
            raise ValueError('The Cloud has no Datacenter in its DatacenterList.')
        for dc in self._dc_list:
            dc.set_cloud(self)

    def start_run(self, env, sim_time):
        self._env = env
        self._sim_time = sim_time
        logging.info(f'Cloud started at {env.now}.')
        yield env.timeout(0)

    def get_dc_list(self):
        return self._dc_list

    def process_vm_create(self, vm):
        logging.info(f'VM creation request for vm_id = {vm.get_id()} received at cloud at {self._env.now}.')
        self._dc_tried = 0
        while self._dc_tried <= len(self._dc_list):
            self._vm_create_events[vm.get_id()] = self._env.event()
            dc = self._dc_selection_policy.select_dc_for_vm(vm)
            logging.info(f'VM with vm_id = {vm.get_id()} sent to datacenter_id = {dc.get_id()}'
                         f' at {self._env.now}.')
            status = dc.process_vm_create(vm)
            #yield self._vm_create_events[vm.get_id()]
            if status:
                self._dc_selection_policy.accept_selection()
                break
            else:
                result = self._dc_selection_policy.reject_selection()
                if result:
                    self._dc_tried = self._dc_tried + 1
                else:
                    logging.warning(f'VM with vm_id = {vm.get_id()} not created on all datacenters')
                    ack = {'type': 'vm_create', 'dest': 'broker', 'vm_id': vm.get_id(),
                           'message': f'VM with vm_id = {vm.get_id()} not created on any datacenter.'}
                    self.send_ack(ack)
                    break
        yield self._env.timeout(0)

    def process_ack(self, ack):
        if ack['status'] == 'created':
            logging.info(ack['message'])
        else:
            logging.warning(ack['message'])
        yield self._env.timeout(0)

    def send_ack(self, ack):
        if ack['dest'] == 'broker':
            self._env.process(self._broker.process_ack(ack))
        yield self._env.timeout(0)

    def set_broker(self, broker):
        self._broker = broker
