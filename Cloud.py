"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""


class Cloud:
    """ Cloud class definition: It is responsible for managing datacenter selection for incoming VMs via its
    datacenter selection policy
    :ivar _env: simulation environment
    :type _env: simpy env
    :ivar _cloud_id: id of this cloud
    :type _cloud_id: int
    :ivar _dc_selection_policy: a policy that determines how datacenters are selected for incoming VMs
    :type _dc_selection_policy: VMAllocationPolicy or its subclasses
    :ivar _last_process_time: ? unused for now
    :type _last_process_time: int
    :ivar _dc_list: list of datacenters in this cloud
    :type _dc_list: list[Datacenter]
    """
    def __init__(self, cloud_attributes, dc_list, dc_selection_policy):
        self._env = None
        self._cloud_id = cloud_attributes['cloud_id']
        self._dc_selection_policy = dc_selection_policy
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

    def get_dc_list(self):
        return self._dc_list
