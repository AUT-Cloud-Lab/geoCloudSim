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
        self._last_selected = 0
        self._agent = agent
        self._num_rejected = 0
        self._terminal = False
        self._evaluation = evaluation
        self._pre_costs = [0]*len(datacenter_list)

    def select_dc_for_vm(self, vm):
        if int(vm.get_id()) == 100:
            self._terminal = True
        # states = [dc.get_power() for dc in self._datacenter_list]
        states = [dc.get_brown_cost(5) for dc in self._datacenter_list]
        self._pre_costs = states
        action = self._agent.act(states=states, independent=self._evaluation)
        log('INFO', -1, f'action = {action}')
        return self._datacenter_list[action]

    def reject_selection(self):
        self._num_rejected += 1
        # states = [dc.get_power() for dc in self._datacenter_list]
        # reward = -(statistics.stdev(states) / statistics.mean(states))
        costs = [dc.get_brown_cost(5) for dc in self._datacenter_list]
        reward = - (sum(costs) - sum(self._pre_costs)) / sum(costs)
        log('INFO', -1, f'reward = {reward}')
        if not self._evaluation:
            self._agent.observe(terminal=self._terminal, reward=reward)

    def accept_selection(self):
        self._num_rejected = 0
        # states = [dc.get_power() for dc in self._datacenter_list]
        # reward = -(statistics.stdev(states) / statistics.mean(states))
        costs = [dc.get_brown_cost(1) for dc in self._datacenter_list]
        reward = - (sum(costs) - sum(self._pre_costs)) / sum(costs)
        log('INFO', -1, f'reward = {reward}')
        if not self._evaluation:
            self._agent.observe(terminal=self._terminal, reward=reward)
