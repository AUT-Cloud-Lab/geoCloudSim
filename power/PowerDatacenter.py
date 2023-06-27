from core.Datacenter import Datacenter
from utils.logger import log_me
from simpy.util import start_delayed


class PowerDatacenter(Datacenter):
    def __init__(self, dc_id, datacenter_attributes, datacenter_power_traces, vm_allocation_policy, host_list):
        super().__init__(dc_id, datacenter_attributes, vm_allocation_policy, host_list)
        self._power = 0
        self._power_traces = datacenter_power_traces

    def process_vm_create(self, vm):
        log_me('INFO', int(self._env.now), 'Datacenter', 'VM creation request received', vm.get_id(),
               self._datacenter_id)
        result = self._vm_allocation_policy.allocate_host_for_vm(vm)
        if result:
            start_delayed(self._env, self.process_vm_destroy(vm), delay=vm.get_duration())
            self.update_power()
            self._vm_list.append(vm.get_vm_uid())
            log_me('INFO', int(self._env.now), 'Datacenter', 'VM created and allocated', vm.get_id(),
                   self._datacenter_id, vm.get_host().get_id())
            log_me('INFO', int(self._env.now), 'Datacenter', f'Now consumes {self._power}W, and hosts {len(self._vm_list)} VMs', vm_id=None,
                   dc_id=self._datacenter_id)
        else:
            log_me('WARN', int(self._env.now), 'Datacenter', 'VM not created', vm.get_id(), self._datacenter_id)
        return result

    def process_vm_destroy(self, vm):
        log_me('INFO', int(self._env.now), 'Datacenter', 'VM destroy request received', vm.get_id(), self._datacenter_id)
        self._vm_allocation_policy.deallocate_host_for_vm(vm)
        self._vm_list.remove(vm.get_vm_uid())
        log_me('INFO', int(self._env.now), 'Datacenter', 'VM destroyed', vm.get_id(), self._datacenter_id)
        self.update_power()
        log_me('INFO', int(self._env.now), 'Datacenter', f'Now consumes {self._power}W, and hosts {len(self._vm_list)} VMs', vm_id=None,
               dc_id=self._datacenter_id)
        yield self._env.timeout(0)

    def update_power(self):
        self._power = 0
        for host in self._host_list:
            self._power += host.get_power()
        self._power = round(self._power * float(self._power_traces['pue'][int(self._env.now)]), 2)

    def get_power(self):
        return self._power
