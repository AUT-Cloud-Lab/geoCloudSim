from abc import ABC

from VMAllocationPolicy import VMAllocationPolicy


class VMAllocationPolicyLeastMips(VMAllocationPolicy):
    """
    This policy tries to allocate a host with minimum available Mips
    """
    def __init__(self, host_list):
        super().__init__(host_list)
        self.__vm_table = dict()

    def allocate_host_for_vm(self, vm):
        suitable_hosts = []
        for host in self.get_host_list():
            if host.is_suitable_for_vm(vm):
                suitable_hosts.append(host)
        available_mips = [host.get_available_mips() for host in suitable_hosts]
        index_min = min(range(len(available_mips)), key=available_mips.__getitem__)
        host = suitable_hosts[index_min]
        return self.allocate_host_for_vm(vm, host)

    def allocate_host_for_vm(self, vm, host):
        if host.vm_create(vm):
            vm_table = self.get_vm_table()
            vm_table[vm.get_vm_uid()] = host
            self._set_vm_table(vm_table)
            return True
        return False

    def optimize_allocation(self, vm_list):
        pass

    def deallocate_host_for_vm(self, vm):
        vm_table = self.get_vm_table()
        del vm_table[vm.get_vm_uid()]
        self._set_vm_table(vm_table)
        host = self.get_host(vm)
        host.vm_destroy(vm)

    def get_host(self, vm):
        return self.get_vm_table()[vm.get_vm_uid()]

    def get_host_list(self):
        return self.__host_list

    def _set_host_list(self, host_list):
        self.__host_list = host_list

    def get_vm_table(self):
        return self.__vm_table

    def _set_vm_table(self, vm_table):
        self.__vm_table = vm_table
