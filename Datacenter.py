class Datacenter:
    def __init__(self, dc_id, datacenter_attributes, vm_allocation_policy, scheduling_interval, host_list):
        self._env = None
        self._arch = datacenter_attributes['arch']
        self._os = datacenter_attributes['os']
        self._vmm = datacenter_attributes['vmm']
        self._time_zone = datacenter_attributes['time_zone']
        self._cost_per_mips = datacenter_attributes['cost_per_mips']
        self._cost_per_ram = datacenter_attributes['cost_per_ram']
        self._cost_per_bw = datacenter_attributes['cost_per_bw']
        self._cost_per_storage = datacenter_attributes['cost_per_storage']
        self._datacenter_id = dc_id
        self._vm_allocation_policy = vm_allocation_policy
        self._scheduling_interval = scheduling_interval
        self._last_process_time = 0
        self._vm_list = []
        self._host_list = host_list
        self._cloud = None
        if not host_list:
            raise ValueError('The Data center has no Host in its HostList')
        for host in self._host_list:
            host.set_datacenter(self)

    def start_run(self, env):
        self._env = env
        print('datacenter started')
        yield env.timeout(1)
        print('datacenter stopped')

    def set_cloud(self, cloud):
        self._cloud = cloud
