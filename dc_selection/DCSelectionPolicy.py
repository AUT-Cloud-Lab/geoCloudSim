"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

from abc import ABC, abstractmethod


class DCSelectionPolicy(ABC):
    def __init__(self, datacenter_list):
        self._datacenter_list = datacenter_list

    @abstractmethod
    def select_dc_for_vm(self, vm):
        pass

    @abstractmethod
    def reject_selection(self):
        pass

    @abstractmethod
    def accept_selection(self):
        pass
