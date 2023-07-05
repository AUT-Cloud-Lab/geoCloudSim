from simpy.util import start_delayed

from core.Datacenter import Datacenter
from utils.logger import log_me, log
from numpy import cumsum, minimum, ones


class PowerDatacenter(Datacenter):
    def __init__(self, dc_id, datacenter_attributes, datacenter_power_traces, vm_allocation_policy, host_list):
        super().__init__(dc_id, datacenter_attributes, vm_allocation_policy, host_list)
        self._power = 0.0
        self._power_all = [0.0]
        self._green_all = [0.0]
        self._brCost_all = [0.0]
        self._pue = list(map(float, datacenter_power_traces['pue']))
        self._solar = list(map(float, datacenter_power_traces['solar']))
        self._battery = datacenter_attributes['battery']
        self._br_price = list(map(float, datacenter_power_traces['br_cost']))



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
        # get current time and update it if necessary
        now = int(self._env.now)
        if now > len(self._br_price) - 1:
            log('WARN', now, 'Simulation time exceeds power traces length!')
            now = len(self._br_price) - 1

        # set current power of data center
        self._power = 0
        for host in self._host_list:
            self._power += host.get_power()
        self._power = round(self._power * self._pue[now], 2)

        # extend power_all history if it is not current
        if now >= len(self._power_all):
            diff = now - len(self._power_all) + 1
            self._power_all.extend([self._power_all[-1]] * diff)
            for i in reversed(range(diff)):
                green = min(self._green_all[now - i - 1] + self._solar[now - i - 1], self._battery)
                rem_green = green - self._power_all[now - i]
                if rem_green < 0:
                    self._brCost_all.append(-rem_green * self._br_price[now - i])
                    self._green_all.append(0)
                else:
                    self._brCost_all.append(0)
                    self._green_all.append(rem_green)
        assert(len(self._power_all) == (now + 1))
        self._power_all[now] = self._power
        green = min(self._green_all[now - 1] + self._solar[now - 1], self._battery)
        rem_green = green - self._power
        if rem_green < 0:
            self._brCost_all[now] = -rem_green * self._br_price[now]
            self._green_all[now] = 0
        else:
            self._brCost_all[now] = 0
            self._green_all[now] = rem_green


    def get_brown_cost(self, num_points=-1):
        # num_points means how many costs should be
        now = int(self._env.now)
        if now > len(self._br_price) - 1:
            log('WARN', now, 'Simulation time exceeds power traces length!')
            now = len(self._br_price) - 1
        if num_points <= 0:
            log('WARN', now, 'Number of points should be greater than 1. All points will be used!')
            st = 0
        else:
            st = now + 1 - num_points
            if st < 0:
                log('WARN', now, 'There are still fewer points than specified!')
                st = 0
        # br_price = self._br_price[st:now + 1]
        self.update_power()
        # power = self.get_power_all()[st:now + 1]
        # green = self._solar[st:now + 1]
        # return sum([max(0.0, (power[i] - green[i]) * br_price[i]) for i in range(len(green))])
        return sum(self._brCost_all[st:now+1])


    def get_max_cost(self):
        power = 0
        for host in self._host_list:
            power += host.get_max_power()
        return round(power * self.get_max_pue() * self.get_max_br_price(), 2)
    def get_reward(self):
        now = int(self._env.now)
        if self._brCost_all[now] > 0:
            return -self._brCost_all[now]
        else:
            return self._green_all[now]

    def get_power(self):
        return self._power

    def get_power_all(self):
        return self._power_all

    def get_br_price(self):
        now = int(self._env.now)
        return self._br_price[now]

    def get_max_br_price(self):
        return max(self._br_price)

    def get_green(self):
        now = int(self._env.now)
        self.update_power()
        return self._green_all[now]

    def get_pue(self):
        now = int(self._env.now)
        return self._pue[now]

    def get_max_pue(self):
        return max(self._pue)

    def get_battery_cap(self):
        return self._battery

    def get_avg_util(self):
        util = 0
        for h in self._host_list:
            util += h.get_avg_util()
        return util / len(self._host_list)