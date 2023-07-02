"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""


from simpy.util import start_delayed
from utils.logger import log_me


class Broker:
    """ Broker class definition: It is responsible for sending VMs request (creation, submission, destruction) to Cloud
    on behalf of users
    :ivar _sim_time: simulation time
    :type _sim_time: int
    :ivar _env: simulation environment
    :type _env: simpy env
    :ivar _vm_list: list of VMs
    :type _vm_list: list[VM]
    :ivar _vms_created_list: list of created VMs
    :type _vms_created_list: list[VM]
    :ivar _vms_requested: number of VM creation requests
    :type _vms_requested: int
    :ivar _vms_ack: number of VM creation request acknowledgement
    :type _vms_ack: int
    :ivar _vms_destroyed: number of VM destroyed
    :type _vms_destroyed: int
    :ivar _datacenter_list: list of datacenters
    :type _datacenter_list: list[Datacenter]
    :ivar _datacenter_requested_ids_list: list of ids of requested datacenters
    :type _datacenter_requested_ids_list: list[int]
    :ivar _vms_datacenter_map: mapping of VMs to datacenters
    :type _vms_datacenter_map: dict<VM, Datacenter>
    :ivar _cloud: the cloud instance that includes all datacenters
    :type _cloud: Cloud
    """
    def __init__(self, cloud):
        """ Constructor
        :param cloud: the cloud instance that includes all datacenters
        """
        self._sim_time = -1
        self._env = None
        self._vm_list = []
        self._vms_created_list = []
        self._vms_requested = 0
        self._vms_ack = 0
        self._vms_destroyed = 0
        self._datacenter_list = cloud.get_dc_list()
        self._datacenter_requested_ids_list = []
        self._vms_datacenter_map = dict()
        self._cloud = cloud

    def submit_vm_list(self, vm_list):
        """ Submit the list of VMs to the broker
        :param vm_list: list of VMs
        """
        self._vm_list.extend(vm_list)

    def start_run(self, env, sim_time):
        """Start the broker event processor
        :param env: the simulation environment
        :param sim_time: the simulation duration
        """
        self._env = env
        self._sim_time = sim_time
        log_me('INFO', int(env.now), 'Broker', 'Started')
        vm_list = sorted(self._vm_list, key=lambda obj: obj.get_arrival_time())
        for vm in vm_list:
            vm_delay = vm.get_arrival_time() - env.now
            assert(vm_delay >= 0)
            request = {'dest': 'cloud', 'type': 'vm_create', 'vm': vm}
            if vm_delay == 0:
                # TODO maybe sending interrupt be better than creating process
                yield env.process(self.send_request(request))
            else:
                yield start_delayed(env, self.send_request(request), delay=vm_delay)
        log_me('INFO', int(env.now), 'Broker', 'Stopped')

    def send_request(self, request):
        """ Sending request (VM creation, etc.) to Cloud/Datacenters
        :param request:  a dictionary containing the request type, destination, etc.
        """
        if request['type'] == 'vm_create' and request['dest'] == 'cloud':
            vm = request['vm']
            log_me('INFO', int(self._env.now), 'Broker', 'VM creation request sent to cloud', vm_id=vm.get_id())
            yield self._env.process(self._cloud.process_vm_create(vm))

    def process_ack(self, ack):
        # Todo: should do somthing with the ack, for example count created/not created VMs
        log_me(ack['kind'], int(self._env.now), 'Broker', ack['message'], vm_id=ack['vm_id'])
        yield self._env.timeout(0)
