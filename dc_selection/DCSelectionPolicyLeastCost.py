"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""
import numpy as np

from dc_selection.DCSelectionPolicy import DCSelectionPolicy


class DCSelectionPolicyLeastCost(DCSelectionPolicy):
    def __init__(self, datacenter_list):
        super().__init__(datacenter_list)
        self._vm_table = dict()
        self._rejected = [0] * len(datacenter_list)
        self._selected = 0

    def select_dc_for_vm(self, vm):
        costs = [dc.get_brown_cost() for dc in self._datacenter_list]
        if sum(self._rejected) == len(self._rejected):
            self._rejected = [0] * len(self._datacenter_list)
        for i in range(len(self._datacenter_list)):
            if self._rejected[i] == 1:
                costs[i] = np.Inf
        self._selected = costs.index(min(costs))
        return self._datacenter_list[self._selected]

    def reject_selection(self):
        self._rejected[self._selected] = 1

    def accept_selection(self):
        self._rejected = [0] * len(self._datacenter_list)
