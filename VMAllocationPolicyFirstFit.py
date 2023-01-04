"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulation framework
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

from VMAllocationPolicy import VMAllocationPolicy


class VMAllocationPolicyFirstFit(VMAllocationPolicy):
    """
    This policy tries to allocate the first host that have enough capacity for the VM
    """
    def __init__(self, host_list):
        super().__init__(host_list)
        self._vm_table = dict()

    def allocate_host_for_vm(self, vm):
        for host in self.get_host_list():
            if host.is_suitable_for_vm(vm):
                if host.vm_create(vm):
                    self._vm_table[vm.get_vm_uid()] = host
                    return True
        print(f'no suitable host for vm with vm_id = {vm.get_id()}')
        return False

    def optimize_allocation(self, vm_list):
        pass

    def deallocate_host_for_vm(self, vm):
        host = self._vm_table.pop(vm.get_vm_uid())
        host.vm_destroy(vm)

    def get_host(self, vm):
        return self._vm_table[vm.get_vm_uid()]

    def get_host_list(self):
        return self._host_list

    def _set_host_list(self, host_list):
        self._host_list = host_list

    def get_vm_table(self):
        return self._vm_table

    def _set_vm_table(self, vm_table):
        self._vm_table = vm_table
