class Cloud:
    def __init__(self, cloud_attributes, dc_list, vm_cloud_allocation_policy):
        self._env = None
        self._name = cloud_attributes['name']
        self._cloud_id = cloud_attributes['cloud_id']
        self._vm_allocation_policy = vm_cloud_allocation_policy
        self._last_process_time = 0
        self._dc_list = dc_list
        if not dc_list:
            raise ValueError('The Cloud has no Datacenter in its DatacenterList')
        for dc in self._dc_list:
            dc.set_cloud(self)

    def start_run(self, env):
        self._env = env
        print('cloud started')
        yield env.timeout(1)
        print('cloud stopped')