"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""


class BwProvisioner:
    """ BwProvisioner class definition: It is responsible for provisioning host bandwidth for VMs
    :ivar _bw: host total bandwidth
    :type _bw: float
    :ivar _available_bw: host available (i.e. remaining) bandwidth
    :type _available_bw: float
    :ivar _bw_table: mapping between VM_id and its allocated bandwidth
    :type _bw_table: dict<vm_id: int, bw: float>
    """
    def __init__(self, bw):
        """ Constructor
        :param bw: total bandwidth of the provisioner
        """
        self._bw = bw
        self._available_bw = bw
        self._bw_table = dict()

    def allocate_bw_for_vm(self, vm, bw):
        """ Allocate a given bandwidth for a given VM
        :param vm: an instance of the VM class
        :param bw: the VM's requested bandwidth
        :return: True: succeeded, False: failed
        :rtype: bool
        """
        self.deallocate_bw_for_vm(vm)
        available_bw = self.get_available_bw()
        if available_bw >= bw:
            self.set_available_bw(available_bw - bw)
            self.get_bw_table()[vm.get_id()] = bw
            vm.set_current_allocated_bw(self.get_allocated_bw_for_vm(vm))
            return True
        vm.set_current_allocated_bw(self.get_allocated_bw_for_vm(vm))
        return False

    def get_allocated_bw_for_vm(self, vm):
        """ Get the amount of bandwidth allocated for a given VM
        :param vm: an instance of the VM class
        :return: the amount of bandwidth
        :rtype: float
        """
        if vm.get_id() in self.get_bw_table():
            return self.get_bw_table()[vm.get_id()]
        return 0

    def deallocate_bw_for_vm(self, vm):
        """ Deallocate bandwidth for a given VM
        :param vm: an instance of the VM class
        """
        bw_table = self.get_bw_table()
        vm_id = vm.get_id()
        if vm_id in bw_table:
            amount_freed = bw_table[vm_id]
            del bw_table[vm_id]
            self.set_bw_table(bw_table)
            self.set_available_bw(self.get_available_bw() + amount_freed)
            vm.set_current_allocated_bw(0)

    def deallocate_bw_for_all_vm(self):
        """ Deallocate bandwidth of all resident VMs"""
        self.set_available_bw(self.get_bw())
        self.set_bw_table(dict())

    def is_suitable_for_vm(self, vm, bw):
        """ Check if the provisioner has enough bandwidth for a given VM
        :param vm: an instance of the VM class
        :param bw: the VM's requested bandwidth
        :return: True: has enough bandwidth False: otherwise
        :rtype: bool
        """
        allocated_bw = self.get_allocated_bw_for_vm(vm)
        result = self.allocate_bw_for_vm(vm, bw)
        self.deallocate_bw_for_vm(vm)
        if allocated_bw > 0:
            self.allocate_bw_for_vm(vm, allocated_bw)
        return result

    def get_bw_table(self):
        """ Get the bandwidth-VM mapping table
        :return: the bandwidth-VM mapping table
        :rtype: dict<vm_id: int, bw: float>
        """
        return self._bw_table

    def set_bw_table(self, bw_table):
        """ Set the bandwidth-VM mapping table of the provisioner
        :param: the bandwidth-VM mapping table
        """
        self._bw_table = bw_table

    def get_bw(self):
        """ Get the total bandwidth of the provisioner
        :return: the bandwidth
        :rtype: float
        """
        return self._bw

    def set_bw(self, bw):
        """ Set the total bandwidth of the provisioner
        :param: the total bandwidth
        """
        self._bw = bw

    def get_available_bw(self):
        """ Get the available bandwidth of the provisioner
        :return: the available bandwidth
        :rtype: float
        """
        return self._available_bw

    def set_available_bw(self, bw):
        """ Set the available bandwidth of the provisioner
        :param: the available bandwidth
        """
        self._available_bw = bw
