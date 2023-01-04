class RamProvisioner:
    def __init__(self, ram):
        self._ram = ram
        self._available_ram = ram
        self._ram_table = dict()

    def allocate_ram_for_vm(self, vm, ram):
        max_ram = vm.get_ram()
        ram = max(ram, max_ram)
        self.deallocate_ram_for_vm(vm)
        available_ram = self.get_available_ram()
        if available_ram >= ram:
            self.set_available_ram(available_ram - ram)
            self.get_ram_table()[vm.get_id()] = ram
            vm.set_current_allocated_ram(self.get_allocated_ram_for_vm(vm))
            return True
        vm.set_current_allocated_ram(self.get_allocated_ram_for_vm(vm))
        return False

    def get_allocated_ram_for_vm(self, vm):
        if vm.get_id() in self.get_ram_table():
            return self.get_ram_table()[vm.get_id()]
        return 0

    def deallocate_ram_for_vm(self, vm):
        ram_table = self.get_ram_table()
        vm_id = vm.get_id()
        if vm_id in ram_table:
            amount_freed = ram_table[vm_id]
            del ram_table[vm_id]
            self.set_ram_table(ram_table)
            self.set_available_ram(self.get_available_ram() + amount_freed)
            vm.set_current_allocated_ram(0)

    def deallocate_ram_for_all_vm(self):
        self.set_available_ram(self.get_ram())
        self.set_ram_table(dict())

    def is_suitable_for_vm(self, vm, ram):
        allocated_ram = self.get_allocated_ram_for_vm(vm)
        result = self.allocate_ram_for_vm(vm, ram)
        self.deallocate_ram_for_vm(vm)
        if allocated_ram > 0:
            self.allocate_ram_for_vm(vm, allocated_ram)
        return result

    def get_ram_table(self):
        return self._ram_table

    def set_ram_table(self, ram_table):
        self._ram_table = ram_table

    def get_ram(self):
        return self._ram

    def set_ram(self, ram):
        self._ram = ram

    def get_available_ram(self):
        return self._available_ram

    def set_available_ram(self, ram):
        self._available_ram = ram

