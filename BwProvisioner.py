class BwProvisioner:
    def __init__(self, bw):
        self._bw = bw
        self._available_bw = bw
        self._bw_table = dict()

    def allocate_bw_for_vm(self, vm, bw):
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
        if vm.get_id() in self.get_bw_table():
            return self.get_bw_table()[vm.get_id()]
        return 0

    def deallocate_bw_for_vm(self, vm):
        bw_table = self.get_bw_table()
        vm_id = vm.get_id()
        if vm_id in bw_table:
            amount_freed = bw_table[vm_id]
            del bw_table[vm_id]
            self.set_bw_table(bw_table)
            self.set_available_bw(self.get_available_bw() + amount_freed)
            vm.set_current_allocated_bw(0)

    def deallocate_bw_for_all_vm(self):
        self.set_available_bw(self.get_bw())
        self.set_bw_table(dict())

    def is_suitable_for_vm(self, vm, bw):
        allocated_bw = self.get_allocated_bw_for_vm(vm)
        result = self.allocate_bw_for_vm(vm, bw)
        self.deallocate_bw_for_vm(vm)
        if allocated_bw > 0:
            self.allocate_bw_for_vm(vm, allocated_bw)
        return result

    def get_bw_table(self):
        return self._bw_table

    def set_bw_table(self, bw_table):
        self._bw_table = bw_table

    def get_bw(self):
        return self._bw

    def set_bw(self, bw):
        self._bw = bw

    def get_available_bw(self):
        return self._available_bw

    def set_available_bw(self, bw):
        self._available_bw = bw
