"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

import math


class Host:
    """ A host (server) is a physical machine inside a data center that can host virtual machines (VMs).
    It provisions RAM, MIPS, Storage and BW for its VMs via its VM allocation policy
    :ivar _host_id: id of host
    :type _host_id: int
    :ivar _ram_provisioner: an instance of RamProvisioner that handles provisioning of RAM to VMs
    :type _ram_provisioner: RamProvisioner
    :ivar _bw_provisioner: an instance of BwProvisioner that handles provisioning of bandwidth to VMs
    :type _bw_provisioner: BwProvisioner
    :ivar _storage_provisioner: an instance of StorageProvisioner that handles provisioning of storage to VMs
    :type _storage_provisioner: StorageProvisioner
    :ivar _mips_provisioner: an instance of MipsProvisioner that handles provisioning of mips to VMs
    :type _mips_provisioner: MipsProvisioner
    :ivar _vm_list: list of VMs allocated to this host
    :type _vm_list: list[VM]
    :ivar _datacenter: a datacenter instance that this host belongs to
    :type _datacenter: Datacenter
    """
    def __init__(self, host_id, ram_provisioner, bw_provisioner, storage_provisioner, mips_provisioner):
        self._host_id = host_id
        self._ram_provisioner = ram_provisioner
        self._bw_provisioner = bw_provisioner
        self._storage_provisioner = storage_provisioner
        self._mips_provisioner = mips_provisioner
        self._vm_list = []
        self._datacenter = None

    def update_vms_processing(self, current_time):
        current_time = [vm.update_vm_processing(current_time, self.get_mips_provisioner().get_allocated_mips_for_vm(vm))
                        for vm in self.get_vm_list()]
        current_time = [math.inf if i < 0 else i for i in current_time]
        return min(current_time)

    def is_suitable_for_vm(self, vm):
        return self.get_mips_provisioner().is_suitable_for_vm(vm, vm.get_mips()) and \
               self.get_storage_provisioner().is_suitable_for_vm(vm, vm.get_storage()) and \
               self.get_ram_provisioner().is_suitable_for_vm(vm, vm.get_ram()) and \
               self.get_bw_provisioner().is_suitable_for_vm(vm, vm.get_bw())

    def vm_create(self, vm):
        if not self.get_bw_provisioner().allocate_bw_for_vm(vm, vm.get_bw()):
            print(f'Allocation of VM # {vm.get_vm_id()} to Host # {self.get_id()} failed by BW')
            return False
        if not self.get_ram_provisioner().allocate_ram_for_vm(vm, vm.get_ram()):
            print(f'Allocation of VM # {vm.get_vm_id()} to Host # {self.get_id()} failed by RAM')
            self.get_bw_provisioner().deallocate_bw_for_vm(vm)
            return False
        if not self.get_mips_provisioner().allocate_mips_for_vm(vm, vm.get_mips()):
            print(f'Allocation of VM # {vm.get_vm_id()} to Host # {self.get_id()} failed by MIPS')
            self.get_bw_provisioner().deallocate_bw_for_vm(vm)
            self.get_ram_provisioner().deallocate_ram_for_vm(vm)
            return False
        if not self.get_storage_provisioner().allocate_storage_for_vm(vm, vm.get_storage()):
            print(f'Allocation of VM # {vm.get_vm_id()} to Host # {self.get_id()} failed by Storage')
            self.get_bw_provisioner().deallocate_bw_for_vm(vm)
            self.get_ram_provisioner().deallocate_ram_for_vm(vm)
            self.get_mips_provisioner().deallocate_mips_for_vm(vm)
            return False

        self._vm_list.append(vm)
        vm.set_host(self)
        return True

    def vm_destroy(self, vm):
        if vm is not None:
            self.vm_deallocate(vm)
            self._vm_list.remove(vm)
            vm.set_host(None)

    def vm_destroy_all(self):
        self.vm_deallocate_all()
        for vm in self.get_vm_list():
            vm.set_host(None)
        self.set_vm_list([])

    def vm_deallocate(self, vm):
        self.get_ram_provisioner().deallocate_ram_for_vm(vm)
        self.get_bw_provisioner().deallocate_bw_for_vm(vm)
        self.get_mips_provisioner().deallocate_mips_for_vm(vm)
        self.get_storage_provisioner().deallocate_storage_for_vm(vm)

    def vm_deallocate_all(self):
        self.get_ram_provisioner().deallocate_ram_for_all_vm()
        self.get_bw_provisioner().deallocate_bw_for_all_vm()
        self.get_mips_provisioner().deallocate_mips_for_all_vm()
        self.get_storage_provisioner().deallocate_storage_for_all_vm()

    def get_vm(self, vm_id, user_id):
        for vm in self.get_vm_list():
            if vm.get_vm_id() == vm_id and vm.get_user_id() == user_id:
                return vm
        return None

    def get_bw(self):
        return self.get_bw_provisioner().get_bw()

    def get_available_bw(self):
        return self.get_bw_provisioner().get_available_bw()

    def get_ram(self):
        return self.get_ram_provisioner().get_ram()

    def get_available_ram(self):
        return self.get_ram_provisioner().get_available_ram()

    def get_mips(self):
        return self.get_mips_provisioner().get_mips()

    def get_available_mips(self):
        return self.get_mips_provisioner().get_available_mips()

    def get_storage(self):
        return self.get_storage_provisioner().get_storage()

    def get_available_storage(self):
        return self.get_storage_provisioner().get_available_storage()

    def get_id(self):
        return self._host_id

    def set_id(self, host_id):
        self._host_id = host_id

    def get_ram_provisioner(self):
        return self._ram_provisioner

    def set_ram_provisioner(self, ram_provisioner):
        self._ram_provisioner = ram_provisioner

    def get_bw_provisioner(self):
        return self._bw_provisioner

    def set_bw_provisioner(self, bw_provisioner):
        self._bw_provisioner = bw_provisioner

    def get_mips_provisioner(self):
        return self._mips_provisioner

    def set_mips_provisioner(self, mips_provisioner):
        self._mips_provisioner = mips_provisioner

    def get_storage_provisioner(self):
        return self._storage_provisioner

    def set_storage_provisioner(self, storage_provisioner):
        self._storage_provisioner = storage_provisioner

    def get_vm_list(self):
        return self._vm_list

    def set_vm_list(self, vm_list):
        self._vm_list = vm_list

    def get_datacenter(self):
        return self._datacenter

    def set_datacenter(self, datacenter):
        self._datacenter = datacenter
