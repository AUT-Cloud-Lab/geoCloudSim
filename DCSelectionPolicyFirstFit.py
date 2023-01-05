"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""


class DCSelectionPolicyFirstFit:
    def __init__(self, datacenter_list):
        self._datacenter_list = datacenter_list
        self._vm_table = dict()
        self._last_selected = 0

    def select_dc_for_vm(self, vm):
        return self._datacenter_list[self._last_selected]

    def reject_selection(self):
        self._last_selected = (self._last_selected + 1) % len(self._datacenter_list)

    def accept_selection(self):
        self._last_selected = 0
