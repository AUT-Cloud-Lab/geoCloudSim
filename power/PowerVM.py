from core.VM import VM


class PowerVM(VM):
    def __init__(self, vm_id, user_id, mips, ram, bw, storage, vmm, arrival_time, duration):
        super().__init__(vm_id, user_id, mips, ram, bw, storage, vmm, arrival_time, duration)
