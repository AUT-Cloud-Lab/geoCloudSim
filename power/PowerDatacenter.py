from simpy.util import start_delayed

from core.Datacenter import Datacenter
from utils.logger import log_me, log


class PowerDatacenter(Datacenter):
    def __init__(self, dc_id, datacenter_attributes, datacenter_power_traces, vm_allocation_policy, host_list):
        super().__init__(dc_id, datacenter_attributes, vm_allocation_policy, host_list)
        self._power = 0
        self._power_all = [0]
        self._pue = list(map(float, datacenter_power_traces['pue']))
        self._green = list(map(float, datacenter_power_traces['solar']))
        self._br_cost = list(map(float, datacenter_power_traces['br_cost']))

    def process_vm_create(self, vm):
        log_me('INFO', int(self._env.now), 'Datacenter', 'VM creation request received', vm.get_id(),
               self._datacenter_id)
        result = self._vm_allocation_policy.allocate_host_for_vm(vm)
        if result:
            start_delayed(self._env, self.process_vm_destroy(vm), delay=vm.get_duration())
            self.update_power()
            # self.update_brown_cost()
            self._vm_list.append(vm.get_vm_uid())
            log_me('INFO', int(self._env.now), 'Datacenter', 'VM created and allocated', vm.get_id(),
                   self._datacenter_id, vm.get_host().get_id())
            log_me('STAT', int(self._env.now), 'Datacenter',
                   f'Now consumes {self._power}W, and hosts {len(self._vm_list)} VMs', vm_id=None,
                   dc_id=self._datacenter_id)
        else:
            log_me('WARN', int(self._env.now), 'Datacenter', 'VM not created', vm.get_id(), self._datacenter_id)
        return result

    def process_vm_destroy(self, vm):
        log_me('INFO', int(self._env.now), 'Datacenter', 'VM destroy request received', vm.get_id(),
               self._datacenter_id)
        self._vm_allocation_policy.deallocate_host_for_vm(vm)
        self._vm_list.remove(vm.get_vm_uid())
        log_me('INFO', int(self._env.now), 'Datacenter', 'VM destroyed', vm.get_id(), self._datacenter_id)
        self.update_power()
        # self.update_brown_cost()
        log_me('STAT', int(self._env.now), 'Datacenter',
               f'Now consumes {self._power}W, and hosts {len(self._vm_list)} VMs', vm_id=None,
               dc_id=self._datacenter_id)
        yield self._env.timeout(0)

    def update_power(self):
        self._power = 0
        now = int(self._env.now)
        if now > len(self._br_cost) - 1:
            log('WARN', now, 'Simulation time exceeds power traces length!')
            now = len(self._br_cost) - 1
        for host in self._host_list:
            self._power += host.get_power()
        self._power = round(self._power * self._pue[now], 2)
        if now >= len(self._power_all):
            diff = now - len(self._power_all) + 1
            self._power_all.extend([self._power_all[-1]] * diff)
        assert(len(self._power_all) == (now + 1))
        self._power_all[now] = self._power


    def get_brown_cost(self, num_points=-1):
        # num_points means how many costs should be
        now = int(self._env.now)
        if now > len(self._br_cost) - 1:
            log('WARN', now, 'Simulation time exceeds power traces length!')
            now = len(self._br_cost) - 1
        if num_points <= 0:
            log('WARN', now, 'Number of points should be greater than 1. All points will be used!')
            st = 0
        else:
            st = now + 1 - num_points
            if st < 0:
                log('WARN', now, 'There are still fewer points than specified!')
                st = 0
        br_cost = self._br_cost[st:now + 1]
        self.update_power()
        power = self.get_power_all()[st:now + 1]
        green = self._green[st:now + 1]
        return sum([max(0.0, (power[i] - green[i]) * br_cost[i]) for i in range(len(green))])

    def get_power(self):
        return self._power

    def get_power_all(self):
        return self._power_all

