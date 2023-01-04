from abc import ABC

from VMAllocationPolicy import VMAllocationPolicy


class VMAllocationPolicyLeastMips(VMAllocationPolicy):
    """
    This policy tries to allocate a host with minimum available Mips
    """
    def __init__(self, host_list):
        super().__init__(host_list)
        self._vm_table = dict()

    def allocate_host_for_vm(self, vm):
        suitable_hosts = []
        for host in self.get_host_list():
            if host.is_suitable_for_vm(vm):
                suitable_hosts.append(host)
        available_mips = [host.get_available_mips() for host in suitable_hosts]
        index_min = min(range(len(available_mips)), key=available_mips.__getitem__)
        host = suitable_hosts[index_min]
        if host.vm_create(vm):
            self._vm_table[vm.get_vm_uid()] = host
            return True
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
