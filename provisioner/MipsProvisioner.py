"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""


class MipsProvisioner:
    """ MipsProvisioner class definition: It is responsible for provisioning host computing power (in terms of mips)
    for VMs
    :ivar _mips: host total mips
    :type _mips: int
    :ivar _available_mips: host available (i.e. remaining) mips
    :type _available_mips: int
    :ivar _mips_table: mapping between VM_id and its allocated mips
    :type _mips_table: dict<vm_id, mips>
    """
    def __init__(self, mips):
        self._mips = mips
        self._available_mips = mips
        self._mips_table = dict()

    def allocate_mips_for_vm(self, vm, mips):
        self.deallocate_mips_for_vm(vm)
        available_mips = self.get_available_mips()
        if available_mips >= mips:
            self.set_available_mips(available_mips - mips)
            self.get_mips_table()[vm.get_id()] = mips
            vm.set_current_allocated_mips(self.get_allocated_mips_for_vm(vm))
            return True
        vm.set_current_allocated_mips(self.get_allocated_mips_for_vm(vm))
        return False

    def get_allocated_mips_for_vm(self, vm):
        if vm.get_id() in self.get_mips_table():
            return self.get_mips_table()[vm.get_id()]
        return 0

    def deallocate_mips_for_vm(self, vm):
        mips_table = self.get_mips_table()
        vm_id = vm.get_id()
        if vm_id in mips_table:
            amount_freed = mips_table[vm_id]
            del mips_table[vm_id]
            self.set_mips_table(mips_table)
            self.set_available_mips(self.get_available_mips() + amount_freed)
            vm.set_current_allocated_mips(0)

    def deallocate_mips_for_all_vm(self):
        self.set_available_mips(self.get_mips())
        self.set_mips_table(dict())

    def is_suitable_for_vm(self, vm, mips):
        allocated_mips = self.get_allocated_mips_for_vm(vm)
        result = self.allocate_mips_for_vm(vm, mips)
        self.deallocate_mips_for_vm(vm)
        if allocated_mips > 0:
            self.allocate_mips_for_vm(vm, allocated_mips)
        return result

    def get_mips_table(self):
        return self._mips_table

    def set_mips_table(self, mips_table):
        self._mips_table = mips_table

    def get_mips(self):
        return self._mips

    def set_mips(self, mips):
        self._mips = mips

    def get_available_mips(self):
        return self._available_mips

    def set_available_mips(self, mips):
        self._available_mips = mips
