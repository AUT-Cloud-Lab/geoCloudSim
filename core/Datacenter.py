"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

import simpy
from simpy.util import start_delayed
from utils.logger import log_me


class Datacenter:
    """ Datacenter class definition: It is responsible for managing VM creation, allocation of host resources to
    created VMs via its VM allocation policy, and VM destruction when VM lifetime ends
    :ivar _sim_time: simulation time
    :type _sim_time: int
    :ivar _env: simulation environment
    :type _env: simpy env
    :ivar _arch: host architecture
    :type _arch: str
    :ivar _os: host os
    :type _os: str
    :ivar _vmm: host Virtual Machine Manager
    :type _arch: str
    :ivar _time_zone: data center time zone
    :type _time_zone: str
    :ivar _cost_per_mips: cost per each unit of mips
    :type _cost_per_mips: int
    :ivar _cost_per_ram: cost per each unit of ram
    :type _cost_per_ram: int
    :ivar _cost_per_bw: cost per each unit of bw
    :type _cost_per_bw: int
    :ivar _cost_per_storage: cost per each unit of storage
    :type _cost_per_storage: int
    :ivar _datacenter_id: id of this datacenter
    :type _datacenter_id: int
    :ivar _vm_allocation_policy: a policy that determines how VMs are allocated to hosts
    :type _vm_allocation_policy: VMAllocationPolicy or its subclasses
    :ivar _scheduling_interval: ? unused for now
    :type _scheduling_interval: int
    :ivar _last_process_time: ? unused for now
    :type _last_process_time: int
    :ivar _vm_list: list of VMs allocated to this datacenter
    :type _vm_list: list[VM]
    :ivar _host_list: list of hosts within this datacenter
    :type _host_list: list[Host]
    :ivar _cloud: an instance of Cloud
    :type _cloud: Cloud
    """

    def __init__(self, dc_id, datacenter_attributes, vm_allocation_policy, host_list):
        self._env = None
        self._sim_time = None
        self._arch = datacenter_attributes['arch']
        self._os = datacenter_attributes['os']
        self._time_zone = datacenter_attributes['time_zone']
        self._cost_per_mips = datacenter_attributes['cost_per_mips']
        self._cost_per_ram = datacenter_attributes['cost_per_ram']
        self._cost_per_bw = datacenter_attributes['cost_per_bw']
        self._cost_per_storage = datacenter_attributes['cost_per_storage']
        self._datacenter_id = dc_id
        self._vm_allocation_policy = vm_allocation_policy
        self._vm_list = []
        self._host_list = host_list
        self._cloud = None
        if not host_list:
            # logging.error('The Data center has no Host in its HostList.')
            raise ValueError('The Data center has no Host in its HostList')
        for host in self._host_list:
            host.set_datacenter(self)

    def start_run(self, env, sim_time):
        self._env = env
        self._sim_time = sim_time
        log_me('INFO', int(env.now), 'Datacenter', 'Started',
               dc_id=self._datacenter_id)
        yield env.timeout(0)

    def set_cloud(self, cloud):
        self._cloud = cloud

    def run(self):
        while True:
            try:
                # logging.info('dc running')
                yield self._env.timeout(self._sim_time - int(self._env.now) - 10)
                # logging.info('dc stopped')
            except simpy.Interrupt:
                print('What?!')
                break

    def process_vm_create(self, vm):
        log_me('INFO', int(self._env.now), 'Datacenter', 'VM creation request received', vm.get_id(), self._datacenter_id)
        result = self._vm_allocation_policy.allocate_host_for_vm(vm)
        if result:
            start_delayed(self._env, self.process_vm_destroy(vm), delay=vm.get_duration())
            self._vm_list.append(vm.get_vm_uid())
            log_me('INFO', int(self._env.now), 'Datacenter', 'VM created and allocated', vm.get_id(), self._datacenter_id, vm.get_host().get_id())
        else:
            log_me('WARN', int(self._env.now), 'Datacenter', 'VM not created', vm.get_id(), self._datacenter_id)
        return result

    def process_vm_destroy(self, vm):
        log_me('INFO', int(self._env.now), 'Datacenter', 'VM destroy request received', vm.get_id(), self._datacenter_id)
        self._vm_allocation_policy.deallocate_host_for_vm(vm)
        self._vm_list.remove(vm.get_vm_uid())
        log_me('INFO', int(self._env.now), 'Datacenter', 'VM destroyed', vm.get_id(), self._datacenter_id)
        yield self._env.timeout(0)

    def send_ack(self, ack):
        pass

    def get_id(self):
        return self._datacenter_id
