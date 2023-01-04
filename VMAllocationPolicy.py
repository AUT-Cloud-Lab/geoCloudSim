from abc import ABC, abstractmethod


class VMAllocationPolicy(ABC):
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
