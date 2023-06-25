"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

from PyCloudSim import PyCloudSim
from core.Host import Host
from provisioner.RamProvisioner import RamProvisioner
from provisioner.BwProvisioner import BwProvisioner
from provisioner.MipsProvisioner import MipsProvisioner
from provisioner.StorageProvisioner import StorageProvisioner
from vm_allocation.VMAllocationPolicyLeastMips import VMAllocationPolicyLeastMips
from dc_selection.DCSelectionPolicyRoundRobin import DCSelectionPolicyRoundRobin
from core.Datacenter import Datacenter
from core.Broker import Broker
from core.Cloud import Cloud
from core.VM import VM
from csv import DictReader
import logging
from logger import enable_logging


def create_vms() -> list[VM]:
    """Create some VMs manually
    :return: list of vms
    :rtype: list[VM]
    """
    vm_list = []
    num_vms = 2
    logging.info(f'Creating {num_vms} VMs.')
    # adding some homogeneous VMs
    mips = 100  # host MIPS
    ram = 256  # host memory(MB)
    storage = 100000  # host storage (MB)
    bw = 1000  # host network bandwidth (MB/s)
    vmm = "Xen"  # Virtual Machine Monitor
    user_id = 1  # same user ID for all VMs
    arrival_time = 0  # same arrival time for all VMs
    duration = 10  # same duration for all VMs
    for vm_id in range(num_vms):
        vm_list.append(VM(vm_id, user_id, mips, ram, bw, storage, vmm))
    return vm_list


def create_vms_from_file(vm_file: str) -> list[VM]:
    """Create some VMs by importing from a file
    :param vm_file: a string that includes the path to the file
    :type vm_file: str
    :return: list of vms
    :rtype: list[VM]
    :raise: raises exception if importing vm_list file fails
    """
    logging.info(f'Importing VMs from file.')
    vm_list = []
    try:
        with open(vm_file, mode='r') as vm_file:
            vm_dict = DictReader(vm_file)
            for row in vm_dict:
                vm_list.append(VM(row['vm_id'], row['user_id'], float(row['mips']), float(row['ram']), float(row['bw']),
                                  float(row['storage']), float(row['arrival_time']),
                                  float(row['duration'])))
    except Exception as err:
        logging.error(f'Unable to import VMs from file. Unexpected {err=}, {type(err)=}')
        raise Exception(f'Unable to import VMs from file. Unexpected {err=}, {type(err)=}')
    return vm_list


def create_datacenter() -> list[Datacenter]:
    """Create some datacenters
    :return: list of datacenters
    :rtype: list[Datacenter]
    """
    dc_list = []
    num_hosts = 1
    num_dcs = 2
    logging.info(f'Creating {num_dcs} datacenters, each with {num_hosts} hosts.')
    # adding some homogeneous hosts
    mips = 1000  # host MIPS
    ram = 2048  # host memory(MB)
    storage = 1000000  # host storage (MB)
    bw = 100000  # host network bandwidth (MB/s)

    for dc_id in range(num_dcs):
        host_list = []
        for host_id in range(num_hosts):
            ram_provisioner = RamProvisioner(ram)
            mips_provisioner = MipsProvisioner(mips)
            storage_provisioner = StorageProvisioner(storage)
            bw_provisioner = BwProvisioner(bw)
            host_list.append(Host(host_id, ram_provisioner, bw_provisioner, storage_provisioner, mips_provisioner))
        datacenter_attributes = {'arch': 'x86', 'os': 'Linux', 'vmm': 'Xen', 'time_zone': 10.0,
                                 'cost_per_mips': 3.0, 'cost_per_ram': 0.05, 'cost_per_storage': 0.001,
                                 'cost_per_bw': 0.0}
        vm_allocation_policy = VMAllocationPolicyLeastMips(host_list)
        dc_list.append(Datacenter(dc_id, datacenter_attributes, vm_allocation_policy, host_list))
    return dc_list


def create_broker(cloud: Cloud) -> Broker:
    """Create a broker that submits VMs to the cloud
    :param cloud: a handle to cloud object
    :type cloud: Cloud
    :return: broker
    :rtype: Broker
    """
    logging.info(f'Creating the broker.')
    return Broker(cloud)


def create_cloud(dc_list: list[Datacenter]) -> Cloud:
    """Create a cloud from the list of data centers
    :param dc_list: list of datacenters
    :type dc_list: list[Datacenter]
    :return: cloud
    :rtype: Cloud
    """
    logging.info(f'Creating the cloud.')
    cloud_attributes = {'cloud_id': 1}
    dc_selection_policy = DCSelectionPolicyRoundRobin(dc_list)
    return Cloud(cloud_attributes, dc_list, dc_selection_policy)


if __name__ == '__main__':
    enable_logging()
    logging.info(f'Initializing PyCloudSim...')

    # 1) Create Datacenter(s) and Cloud
    datacenters = create_datacenter()
    cloud = create_cloud(datacenters)

    # 2) Create VM(s) either manually or from a file
    vms = create_vms_from_file('csv/vms_test.csv')
    # vms = create_vms()

    # 3) Create a Broker and submit VMs to it
    broker = create_broker(cloud)
    broker.submit_vm_list(vms)
    cloud.set_broker(broker)

    # 4) Create and initialize simulation environment and event processors
    sim_time = 10000
    sim = PyCloudSim(sim_time, broker, cloud, vms)

    # 5) Start the simulation
    sim.start_simulation()

    # 5) Stop the simulation and finalize Results
    sim.stop_simulation()
