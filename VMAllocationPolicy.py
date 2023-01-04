"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

from abc import ABC, abstractmethod


class VMAllocationPolicy(ABC):
    """ VMAllocationPolicy class definition: It is responsible for allocate/deallocate a host for a VM
        :ivar _host_list: a list of all hosts within a data center
        :type _host_list: list[Host]
    """
    def __init__(self, host_list):
        self._host_list = host_list

    @abstractmethod
    def allocate_host_for_vm(self, vm):
        pass

    @abstractmethod
    def optimize_allocation(self, vm_list):
        pass

    @abstractmethod
    def deallocate_host_for_vm(self, vm):
        pass

    @abstractmethod
    def get_host(self, vm):
        pass

    def get_host_list(self):
        return self.__host_list

    def _set_host_list(self, host_list):
        self.__host_list = host_list
