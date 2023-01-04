import simpy
from simpy.util import start_delayed
import logging


class Datacenter:
    def __init__(self, dc_id, datacenter_attributes, vm_allocation_policy, scheduling_interval, host_list):
        self._env = None
        self._sim_time = None
        self._arch = datacenter_attributes['arch']
        self._os = datacenter_attributes['os']
        self._vmm = datacenter_attributes['vmm']
        self._time_zone = datacenter_attributes['time_zone']
        self._cost_per_mips = datacenter_attributes['cost_per_mips']
        self._cost_per_ram = datacenter_attributes['cost_per_ram']
        self._cost_per_bw = datacenter_attributes['cost_per_bw']
        self._cost_per_storage = datacenter_attributes['cost_per_storage']
        self._datacenter_id = dc_id
        self._vm_allocation_policy = vm_allocation_policy
        self._scheduling_interval = scheduling_interval
        self._last_process_time = 0
        self._vm_list = []
        self._host_list = host_list
        self._cloud = None
        if not host_list:
            logging.error('The Data center has no Host in its HostList.')
            raise ValueError('The Data center has no Host in its HostList')
        for host in self._host_list:
            host.set_datacenter(self)

    def start_run(self, env, sim_time):
        self._env = env
        self._sim_time = sim_time
        logging.info('Datacenter process started.')
        # yield env.timeout(1)
        logging.info('Datacenter process stopped.')

    def set_cloud(self, cloud):
        self._cloud = cloud

    def run(self):
        while True:
            try:
                logging.info('dc running')
                yield self._env.timeout(self._sim_time - self._env.now - 10)
                logging.info('dc stopped')
            except simpy.Interrupt:
                print('What?!')
                break

    def process_vm_create(self, env, vm):
        logging.info(f'VM creation request for vm_id = {vm.get_id()} received at {env.now}.')
        result = self._vm_allocation_policy.allocate_host_for_vm(vm)
        if result:
            logging.info(f'VM with vm_id = {vm.get_id()} created and allocated to host_id = {vm.get_host().get_id()} of' 
                         f' datacenter_id = {self._datacenter_id} at {env.now}.')
            start_delayed(env, self.process_vm_destroy(env, vm), delay=vm.get_duration())
        else:
            logging.info(f'VM with vm_id = {vm.get_id()} not created.')
        yield env.timeout(0)

    def process_vm_destroy(self, env, vm):
        logging.info(f'VM destroy request for vm_id = {vm.get_id()} received at {env.now}.')
        self._vm_allocation_policy.deallocate_host_for_vm(vm)
        logging.info(f'VM with vm_id = {vm.get_id()} destroyed at {env.now}.')
        yield env.timeout(0)
