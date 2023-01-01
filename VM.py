class VM:
    """
    Represents a Virtual Machine (VM) that runs inside a Host, sharing host resources with other VMs
    """
    def __init__(self, vm_id, user_id, mips, ram, bw, storage, vmm):
        self._vm_id = vm_id
        self._user_id = user_id
        self._vm_uid = user_id + '-' + vm_id
        self._mips = mips
        self._ram = ram
        self._bw = bw
        self._storage = storage
        self._vmm = vmm
        self._current_allocated_bw = 0
        self._current_allocated_mips = None
        self._current_allocated_ram = 0
        self._current_allocated_storage = 0
        self._host = None

    def get_vm_id(self):
        return self._vm_id

    def set_vm_id(self, vm_id):
        self._vm_id = vm_id

    def get_vm_uid(self):
        return self._vm_uid

    def set_vm_uid(self, uid):
        self._vm_uid = uid

    def get_user_id(self):
        return self._user_id

    def set_user_id(self, user_id):
        self._user_id = user_id

    def get_mips(self):
        return self._mips

    def set_mips(self, mips):
        self._mips = mips

    def get_ram(self):
        return self._ram

    def set_ram(self, ram):
        self._ram = ram

    def get_bw(self):
        return self._bw

    def set_bw(self, bw):
        self._bw = bw

    def get_storage(self):
        return self._storage

    def set_storage(self, storage):
        self._storage = storage

    def get_vmm(self):
        return self._vmm

    def set_vmm(self, vmm):
        self._vmm = vmm

    def get_current_allocated_bw(self):
        return self._current_allocated_bw

    def set_current_allocated_bw(self, current_allocated_bw):
        self._current_allocated_bw = current_allocated_bw

    def get_current_allocated_mips(self):
        return self._current_allocated_mips

    def set_current_allocated_mips(self, current_allocated_mips):
        self._current_allocated_mips = current_allocated_mips

    def get_current_allocated_ram(self):
        return self._current_allocated_ram

    def set_current_allocated_ram(self, current_allocated_ram):
        self._current_allocated_ram = current_allocated_ram

    def get_current_allocated_storage(self):
        return self._current_allocated_storage

    def set_current_allocated_storage(self, current_allocated_storage):
        self._current_allocated_storage = current_allocated_storage

    def get_host(self):
        return self._host

    def set_host(self, host):
        self._host = host
