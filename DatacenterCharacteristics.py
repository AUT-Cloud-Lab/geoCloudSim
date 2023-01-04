"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulation framework
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""


class DatacenterCharacteristics:
    def __init__(self, architecture, os, vmm, host_list, time_zone, cost_per_mips, cost_per_ram, cost_per_bw,
                 cost_per_storage, allocation_policy):
        self.__architecture = architecture
        self.__os = os
        self.__vmm = vmm
        self.__host_list = host_list
        self.__time_zone = time_zone
        self.__cost_per_mips = cost_per_mips
        self.__cost_per_ram = cost_per_ram
        self.__cost_per_bw = cost_per_bw
        self.__cost_per_storage = cost_per_storage
        self.__allocation_policy = allocation_policy
        self.__datacenter_id = -1

    def get_architecture(self):
        return self.__architecture

    def _set_architecture(self, architecture):
        self.__architecture = architecture

    def get_os(self):
        return self.__os

    def _set_os(self, os):
        self.__os = os

    def get_vmm(self):
        return self.__vmm

    def _set_vmm(self, vmm):
        self.__vmm = vmm

    def get_host_list(self):
        return self.__host_list

    def _set_host_list(self, host_list):
        self.__host_list = host_list

    def get_time_zone(self):
        return self.__time_zone

    def _set_time_zone(self, time_zone):
        self.__time_zone = time_zone

    def get_cost_per_mips(self):
        return self.__cost_per_mips

    def _set_cost_per_mips(self, cost_per_mips):
        self.__cost_per_mips = cost_per_mips

    def get_cost_per_ram(self):
        return self.__cost_per_ram

    def _set_cost_per_ram(self, cost_per_ram):
        self.__cost_per_ram = cost_per_ram

    def get_cost_per_bw(self):
        return self.__cost_per_bw

    def _set_cost_per_bw(self, cost_per_bw):
        self.__cost_per_bw = cost_per_bw

    def get_cost_per_storage(self):
        return self.__cost_per_storage

    def _set_cost_per_storage(self, cost_per_storage):
        self.__cost_per_storage = cost_per_storage

    def get_allocation_policy(self):
        return self.__allocation_policy

    def _set_allocation_policy(self, allocation_policy):
        self.__allocation_policy = allocation_policy

    def get_datacenter_id(self):
        return self.__datacenter_id

    def _set_datacenter_id(self, datacenter_id):
        self.__datacenter_id = datacenter_id
