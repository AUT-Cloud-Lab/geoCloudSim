from core.Host import Host
import logging


class PowerHost(Host):
    def __init__(self, host_id, ram_provisioner, bw_provisioner, storage_provisioner, mips_provisioner, power_model):
        super().__init__(host_id, ram_provisioner, bw_provisioner, storage_provisioner, mips_provisioner)
        self._power_model = power_model
        self._power = 0

    def get_power(self):
        return self._power_model.get_power(self.get_mips_util(), self.get_ram_util(), self.get_bw_util(),
                                           self.get_storage_util())

    def get_max_power(self):
        return self._power_model.get_power(1, 1, 1, 1)

    # def get_energy(self, from_util, to_util, time):
    #     return time * (self.get_power(from_util) + self.get_power(to_util))/2
    def get_mips_util(self):
        return (self.get_mips() - self.get_available_mips()) / self.get_mips() if self.get_mips() != 0 else 0

    def get_ram_util(self):
        return (self.get_ram() - self.get_available_ram()) / self.get_ram() if self.get_ram() != 0 else 0

    def get_bw_util(self):
        return (self.get_bw() - self.get_available_bw()) / self.get_bw() if self.get_bw() != 0 else 0

    def get_storage_util(self):
        return (self.get_storage() - self.get_available_storage()) / self.get_storage() if self.get_storage() != 0 else 0

    def vm_create(self, vm):
        if not self.get_bw_provisioner().allocate_bw_for_vm(vm, vm.get_bw()):
            logging.warning(f'Allocation of VM # {vm.get_vm_id()} to Host # {self.get_id()} failed by BW')
            return False
        if not self.get_ram_provisioner().allocate_ram_for_vm(vm, vm.get_ram()):
            logging.warning(f'Allocation of VM # {vm.get_vm_id()} to Host # {self.get_id()} failed by RAM')
            self.get_bw_provisioner().deallocate_bw_for_vm(vm)
            return False
        if not self.get_mips_provisioner().allocate_mips_for_vm(vm, vm.get_mips()):
            logging.warning(f'Allocation of VM # {vm.get_vm_id()} to Host # {self.get_id()} failed by MIPS')
            self.get_bw_provisioner().deallocate_bw_for_vm(vm)
            self.get_ram_provisioner().deallocate_ram_for_vm(vm)
            return False
        if not self.get_storage_provisioner().allocate_storage_for_vm(vm, vm.get_storage()):
            logging.warning(f'Allocation of VM # {vm.get_vm_id()} to Host # {self.get_id()} failed by Storage')
            self.get_bw_provisioner().deallocate_bw_for_vm(vm)
            self.get_ram_provisioner().deallocate_ram_for_vm(vm)
            self.get_mips_provisioner().deallocate_mips_for_vm(vm)
            return False
        self._power = self.get_power()
        self._vm_list.append(vm)
        vm.set_host(self)
        return True
