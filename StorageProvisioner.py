"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""


class StorageProvisioner:
    """ StorageProvisioner class definition: It is responsible for provisioning host storage for VMs
    :ivar _storage: host total storage
    :type _storage: int
    :ivar _available_storage: host available (i.e. remaining) storage
    :type _available_storage: int
    :ivar _storage_table: mapping between VM_id and its allocated storage
    :type _storage_table: dict<vm_id, storage>
    """
    def __init__(self, storage):
        self._storage = storage
        self._available_storage = storage
        self._storage_table = dict()

    def allocate_storage_for_vm(self, vm, storage):
        self.deallocate_storage_for_vm(vm)
        available_storage = self.get_available_storage()
        if available_storage >= storage:
            self.set_available_storage(available_storage - storage)
            self.get_storage_table()[vm.get_id()] = storage
            vm.set_current_allocated_storage(self.get_allocated_storage_for_vm(vm))
            return True
        vm.set_current_allocated_storage(self.get_allocated_storage_for_vm(vm))
        return False

    def get_allocated_storage_for_vm(self, vm):
        if vm.get_id() in self.get_storage_table():
            return self.get_storage_table()[vm.get_id()]
        return 0

    def deallocate_storage_for_vm(self, vm):
        storage_table = self.get_storage_table()
        vm_id = vm.get_id()
        if vm_id in storage_table:
            amount_freed = storage_table[vm_id]
            del storage_table[vm_id]
            self.set_storage_table(storage_table)
            self.set_available_storage(self.get_available_storage() + amount_freed)
            vm.set_current_allocated_storage(0)

    def deallocate_storage_for_all_vm(self):
        self.set_available_storage(self.get_storage())
        self.set_storage_table(dict())

    def is_suitable_for_vm(self, vm, storage):
        allocated_storage = self.get_allocated_storage_for_vm(vm)
        result = self.allocate_storage_for_vm(vm, storage)
        self.deallocate_storage_for_vm(vm)
        if allocated_storage > 0:
            self.allocate_storage_for_vm(vm, allocated_storage)
        return result

    def get_storage_table(self):
        return self._storage_table

    def set_storage_table(self, storage_table):
        self._storage_table = storage_table

    def get_storage(self):
        return self._storage

    def set_bw(self, storage):
        self._storage = storage

    def get_available_storage(self):
        return self._available_storage

    def set_available_storage(self, storage):
        self._available_storage = storage
