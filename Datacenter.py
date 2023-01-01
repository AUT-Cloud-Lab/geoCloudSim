class Datacenter:
    def __init__(self, name, datacenter_characteristics, vm_allocation_policy, scheduling_interval):
        self._name = name
        self._datacenter_characteristics = datacenter_characteristics
        self._vm_allocation_policy = vm_allocation_policy
        self._scheduling_interval = scheduling_interval
        self._last_process_time = 0
        self._vm_list = []
        host_list = self.get_datecenter_characteristics().get_host_list()
        if not host_list:
            raise ValueError('The Data center has no Host in its HostList')
        for host in host_list:
            host.set_datacenter(self)


