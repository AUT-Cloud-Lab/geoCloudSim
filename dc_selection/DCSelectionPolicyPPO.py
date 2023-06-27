"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""
import random
import statistics
from utils.logger import log_rl

from Config import Config as conf

from dc_selection.DCSelectionPolicy import DCSelectionPolicy


class DCSelectionPolicyPPO(DCSelectionPolicy):
    def __init__(self, datacenter_list, agent):
        super().__init__(datacenter_list)
        self._vm_table = dict()
        self._last_selected = 0
        self._agent = agent
        self._num_rejected = 0
        self._terminal = False
        self._action = 0

    def select_dc_for_vm(self, vm):
        if int(vm.get_id()) == 100:
            self._terminal = True
        states = [dc.get_power() for dc in self._datacenter_list]
        action = self._agent.act(states=states)
        self._action = action
        log_rl(f'action = {action}')
        return self._datacenter_list[action]

    def reject_selection(self):
        self._num_rejected += 1
        states = [dc.get_power() for dc in self._datacenter_list]
        reward = self._action
        log_rl(f'reward = {reward}')
        self._agent.observe(terminal=self._terminal, reward=reward)

    def accept_selection(self):
        self._num_rejected = 0
        states = [dc.get_power() for dc in self._datacenter_list]
        reward = self._action
        log_rl(f'reward = {reward}')
        self._agent.observe(terminal=self._terminal, reward=reward)



