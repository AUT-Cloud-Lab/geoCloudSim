"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""
from dc_selection.DCSelectionPolicy import DCSelectionPolicy
from utils.logger import log


class DCSelectionPolicyPPO(DCSelectionPolicy):
    def __init__(self, datacenter_list, agent, evaluation=False):
        super().__init__(datacenter_list)
        self._vm_table = dict()
        self._agent = agent
        self._terminal = False
        self._evaluation = evaluation
        self._pre_costs = [0] * len(datacenter_list)
        self._action = None
        self._req_size = 0
        self._rejected = [0] * len(datacenter_list)

    def select_dc_for_vm(self, vm):
        if int(vm.get_id()) == 100:  # should be updated based on the number of vms in workload
            self._terminal = True
        self._req_size = 0.7 * vm.get_mips() / 36 + 0.24 * vm.get_ram() / 512 + 0.06 * vm.get_bw() / 4048
        # states = [dc.get_power() for dc in self._datacenter_list]
        state_cost = [dc.get_brown_cost(1) / dc.get_max_cost() for dc in self._datacenter_list]
        state_br = [dc.get_br_price() / dc.get_max_br_price() for dc in self._datacenter_list]
        state_gr = [dc.get_green() / dc.get_battery_cap() for dc in self._datacenter_list]
        state_pue = [dc.get_pue() / dc.get_max_pue() for dc in self._datacenter_list]
        state_suitable = list(map(float, [dc.is_suitable_for_vm(vm) for dc in self._datacenter_list]))
        state_util = list(map(float, [dc.get_avg_util() for dc in self._datacenter_list]))
        for i in range(len(state_cost)):
            assert (0 <= state_cost[i] <= 1 and 0 <= state_br[i] <= 1 and 0 <= state_gr[i] <= 1 and 0 <= state_pue[i] <= 1 and 0 <= state_util[i] <= 1)
        self._pre_costs = state_cost
        states = state_cost
        # for i in range(len(states)):
        #     if self._rejected[i] == 1:
        #         states[i] += 10000000
        states.extend(state_br)
        states.extend(state_gr)
        states.extend(state_pue)
        states.extend(state_suitable)
        states.extend(state_util)
        action = self._agent.act(states=states, independent=self._evaluation)
        self._action = action
        log('INFO', -1, f'action = {action}')
        return self._datacenter_list[action]

    def reject_selection(self):
        if self._rejected[self._action] == 1:
            reward = -1000000000
        else:
            reward = -100000000
        self._rejected[self._action] = 1
        # states = [dc.get_power() for dc in self._datacenter_list]
        # reward = -(statistics.stdev(states) / statistics.mean(states))
        # costs = self._datacenter_list[self._action].get_brown_cost(1)
        costs = self._datacenter_list[self._action].get_reward()
        # reward = - (costs - self._pre_costs[self._action]) / self._req_size
        if costs < 0:
            reward += -(-costs - self._pre_costs[self._action]) / self._req_size
        else:
            reward += costs / self._req_size
        log('INFO', -1, f'reward = {reward}')
        if not self._evaluation:
            self._agent.observe(terminal=self._terminal, reward=reward)

    def accept_selection(self):
        self._rejected = [0] * len(self._datacenter_list)
        # states = [dc.get_power() for dc in self._datacenter_list]
        # reward = -(statistics.stdev(states) / statistics.mean(states))
        # costs = self._datacenter_list[self._action].get_brown_cost(1)
        costs = self._datacenter_list[self._action].get_reward()
        # reward = - (costs - self._pre_costs[self._action]) / self._req_size
        if costs < 0:
            reward = -(-costs - self._pre_costs[self._action]) / self._req_size
        else:
            reward = costs / self._req_size
        log('INFO', -1, f'reward = {reward}')
        if not self._evaluation:
            self._agent.observe(terminal=self._terminal, reward=reward)
