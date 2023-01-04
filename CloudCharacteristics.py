"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulation framework
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""


class CloudCharacteristics:
    def __init__(self, cloud_attributes, datacenter_list, allocation_policy):
        self._datacenter_list = datacenter_list
        self._allocation_policy = allocation_policy
        self._cloud_id = cloud_attributes['cloud_id']
        self._name = cloud_attributes['name']

    def get_datacenter_list(self):
        return self._datacenter_list

    def _set_datacenter_list(self, datacenter_list):
        self._datacenter_list = datacenter_list

    def _set_allocation_policy(self, allocation_policy):
        self._allocation_policy = allocation_policy

    def get_datacenter_id(self):
        return self._datacenter_id

    def _set_cloud_id(self, cloud_id):
        self._cloud_id = cloud_id
