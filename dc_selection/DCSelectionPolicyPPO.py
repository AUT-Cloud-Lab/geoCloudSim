"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""
import random
import statistics
from utils.logger import log
from dc_selection.DCSelectionPolicy import DCSelectionPolicy


class DCSelectionPolicyPPO(DCSelectionPolicy):
    def __init__(self, datacenter_list, agent, evaluation=False):
        super().__init__(datacenter_list)
        self._vm_table = dict()
        self._agent = agent
        self._terminal = False
        self._evaluation = evaluation
        self._pre_costs = [0]*len(datacenter_list)
        self._action = None

    def select_dc_for_vm(self, vm):
        if int(vm.get_id()) == 100:
            self._terminal = True
        # states = [dc.get_power() for dc in self._datacenter_list]
        states_cost = [dc.get_brown_cost(5) for dc in self._datacenter_list]
        states_br = [dc.get_br_price() for dc in self._datacenter_list]
        states_gr = [dc.get_green() for dc in self._datacenter_list]
        states_pue = [dc.get_pue() for dc in self._datacenter_list]
        self._pre_costs = states_cost
        states = states_cost
        states.extend(states_br)
        states.extend(states_gr)
        states.extend(states_pue)
        action = self._agent.act(states=states, independent=self._evaluation)
        self._action = action
        log('INFO', -1, f'action = {action}')
        return self._datacenter_list[action]

    def reject_selection(self):
        # states = [dc.get_power() for dc in self._datacenter_list]
        # reward = -(statistics.stdev(states) / statistics.mean(states))
        costs = [dc.get_brown_cost(1) for dc in self._datacenter_list]
        # reward = - (sum(costs) - sum(self._pre_costs)) / sum(costs)
        reward = self._pre_costs[self._action]/costs[self._action]
        log('INFO', -1, f'reward = {reward}')
        if not self._evaluation:
            self._agent.observe(terminal=self._terminal, reward=reward)

    def accept_selection(self):
        # states = [dc.get_power() for dc in self._datacenter_list]
        # reward = -(statistics.stdev(states) / statistics.mean(states))
        costs = [dc.get_brown_cost(1) for dc in self._datacenter_list]
        reward = self._pre_costs[self._action]/costs[self._action]
        log('INFO', -1, f'reward = {reward}')
        if not self._evaluation:
            self._agent.observe(terminal=self._terminal, reward=reward)
