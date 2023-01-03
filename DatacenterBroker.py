class DatacenterBroker:
    def __init__(self):
        self._env = None
        self._vm_list = []
        self._vms_created_list = []
        self._vms_requested = 0
        self._vms_acks = 0
        self._vms_destroyed = 0
        self._datacenter_ids_list = []
        self._datacenter_requested_ids_list = []
        self._vms_datacenter_map = dict()
        self._datacenter_characteristics_map = dict()

    def submit_vm_list(self, vm_list):
        [self._vm_list.append(vm) for vm in vm_list]

    def start_run(self, env):
        self._env = env
        print('broker started')
        yield self._env.timeout(2)
        print('broker stopped')

