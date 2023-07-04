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
        return round((self.get_mips() - self.get_available_mips()) / self.get_mips(), 2) if self.get_mips() != 0 else 0

    def get_ram_util(self):
        return round((self.get_ram() - self.get_available_ram()) / self.get_ram(), 2) if self.get_ram() != 0 else 0

    def get_bw_util(self):
        return round((self.get_bw() - self.get_available_bw()) / self.get_bw(), 2) if self.get_bw() != 0 else 0

    def get_storage_util(self):
        return round((self.get_storage() - self.get_available_storage()) / self.get_storage(), 2) if self.get_storage() != 0 else 0

    def vm_create(self, vm):
        status = super().vm_create(vm)
        if status:
            self._power = self.get_power()
        return status

    def vm_destroy(self, vm):
        super().vm_destroy(vm)
        self._power = self.get_power()
