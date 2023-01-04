import simpy
from simpy.util import start_delayed


class Broker:
    def __init__(self, cloud):
        self._sim_time = None
        self._env = None
        self._vm_list = []
        self._vms_created_list = []
        self._vms_requested = 0
        self._vms_acks = 0
        self._vms_destroyed = 0
        self._datacenter_list = cloud.get_dc_list()
        self._datacenter_requested_ids_list = []
        self._vms_datacenter_map = dict()
        self._cloud = cloud
        # self._datacenter_characteristics_map = dict()

    def submit_vm_list(self, vm_list):
        [self._vm_list.append(vm) for vm in vm_list]

    def start_run(self, env, sim_time):
        self._env = env
        self._sim_time = sim_time
        print(f'broker started at {env.now}')
        dc = self._datacenter_list[0]
        for vm in self._vm_list:
            vm_delay = vm.get_arrival_time() - env.now
            request = {'dest': 'datacenter', 'type': 'vm_create', 'vm': vm, 'dc': dc}
            if vm_delay == 0:
                yield env.process(self.send_request(env, request))
            else:
                yield start_delayed(env, self.send_request(env, request), delay=vm_delay)

        #
        # dc.start_run(env, sim_time)
        # yield self._env.process(dc.run())

        print(f'broker stopped at {env.now}')

    def send_request(self, env, request):
        if request['type'] == 'vm_create':
            dc = request['dc']
            vm = request['vm']
            print(f'vm request with vm_id = {vm.get_id()} sent at {env.now}')
            yield env.process(dc.process_vm_create(env, vm))
            print(f'vm request with vm_id = {vm.get_id()} completed at {env.now}')



    def run(self):
        while True:
            try:
                yield self._env.timeout(self._sim_time - self._env.now)
            except simpy.Interrupt:
                print('What?!')

    def process_event(self, event):
        pass
