"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

import logging
from csv import DictReader, reader
from utils.parser import parse
from utils.plotter import plot_results
from Config import Config as conf
from PyCloudSim import PyCloudSim
from core.Broker import Broker
from core.Cloud import Cloud
from core.VM import VM
from dc_selection.DCSelectionPolicyFirstFit import DCSelectionPolicyFirstFit
from dc_selection.DCSelectionPolicyRoundRobin import DCSelectionPolicyRoundRobin
from utils.logger import enable_logging
from power.PowerDatacenter import PowerDatacenter
from power.PowerHost import PowerHost
from power.models.PowerModelLinear import PowerModelLinear
from provisioner.BwProvisioner import BwProvisioner
from provisioner.MipsProvisioner import MipsProvisioner
from provisioner.RamProvisioner import RamProvisioner
from provisioner.StorageProvisioner import StorageProvisioner
from vm_allocation.VMAllocationPolicyLeastMips import VMAllocationPolicyLeastMips
from vm_allocation.VMAllocationPolicyFirstFit import VMAllocationPolicyFirstFit


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
    user_id = 1  # same user ID for all VMs
    arrival_time = 0  # same arrival time for all VMs
    duration = 10  # same duration for all VMs
    for vm_id in range(num_vms):
        vm_list.append(VM(vm_id, user_id, mips, ram, bw, storage, arrival_time, duration))
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


def create_datacenter() -> list[PowerDatacenter]:
    """Create some datacenters
    :return: list of datacenters
    :rtype: list[Datacenter]
    """
    dc_list = []
    num_hosts = conf.num_hosts
    num_dcs = conf.num_dcs
    logging.info(f'Creating {num_dcs} datacenters, each with {num_hosts} hosts.')
    # adding some homogeneous hosts
    mips, ram, bw, storage = conf.mips, conf.ram, conf.bw, conf.storage
    max_power, stat_power = conf.max_power, conf.stat_power
    mips_power_ratio, ram_power_ratio, bw_power_ratio, storage_power_ratio = conf.mips_pr, conf.ram_pr, conf.bw_pr, conf.storage_pr
    for dc_id in range(num_dcs):
        host_list = []
        for host_id in range(num_hosts):
            ram_provisioner = RamProvisioner(ram)
            mips_provisioner = MipsProvisioner(mips)
            storage_provisioner = StorageProvisioner(storage)
            bw_provisioner = BwProvisioner(bw)
            power_model = PowerModelLinear(max_power, stat_power, mips_power_ratio, ram_power_ratio,
                                           bw_power_ratio, storage_power_ratio)
            host_list.append(
                PowerHost(host_id, ram_provisioner, bw_provisioner, storage_provisioner, mips_provisioner, power_model))
        datacenter_attributes = conf.dc_attributes
        match conf.vm_allocation_policy:
            case 'FirstFit': vm_allocation_policy = VMAllocationPolicyFirstFit(host_list)
            case 'LeastMips': vm_allocation_policy = VMAllocationPolicyLeastMips(host_list)
            case default: raise ValueError('VM allocation policy not implemented')
        dc_list.append(
            PowerDatacenter(dc_id, datacenter_attributes, vm_allocation_policy, host_list))
    return dc_list


def create_datacenter_from_file(dc_file: str, pue_file: str, br_cost_file: str, solar_file: str) -> list[PowerDatacenter]:
    logging.info(f'Importing datacenters and their hosts from file.')
    dc_list = []
    dc_list_dict = {}
    try:
        with open(dc_file, mode='r') as dc_file, open(pue_file, mode='r') as pue_file, \
                open(br_cost_file, mode='r') as br_cost_file, open(solar_file, mode='r') as solar_file:
            dc_dict = DictReader(dc_file)
            pue_list = list(reader(pue_file))
            br_cost_list = list(reader(br_cost_file))
            solar_list = list(reader(solar_file))
            host_id_start = dict()
            for row in dc_dict:
                host_list = []
                if row['dc_id'] not in host_id_start:
                    host_id_start[row['dc_id']] = 0
                for host_id in range(host_id_start[row['dc_id']], host_id_start[row['dc_id']]+int(row['num_host'])):
                    ram_provisioner = RamProvisioner(float(row['ram']))
                    mips_provisioner = MipsProvisioner(float(row['mips']))
                    storage_provisioner = StorageProvisioner(float(row['storage']))
                    bw_provisioner = BwProvisioner(float(row['bw']))
                    power_model = PowerModelLinear(float(row['max_power']), float(row['stat_power']), float(row['mips_pr']), float(row['ram_pr']),
                                                   float(row['bw_pr']), float(row['storage_pr']))
                    host_list.append(
                        PowerHost(host_id, ram_provisioner, bw_provisioner, storage_provisioner, mips_provisioner,
                                  power_model))
                if row['dc_id'] in dc_list_dict.keys():
                    dc_list_dict[row['dc_id']][0].extend(host_list)
                else:
                    dc_attributes = conf.dc_attributes
                    dc_power_traces = dict()
                    dc_power_traces['solar'] = solar_list[int(row['dc_id'])-1]
                    dc_power_traces['br_cost'] = br_cost_list[int(row['dc_id'])-1]
                    dc_power_traces['pue'] = pue_list[int(row['dc_id'])-1]
                    match conf.vm_allocation_policy:
                        case 'FirstFit':
                            vm_allocation_policy = VMAllocationPolicyFirstFit(host_list)
                        case 'LeastMips':
                            vm_allocation_policy = VMAllocationPolicyLeastMips(host_list)
                        case default:
                            raise ValueError('VM allocation policy not implemented')
                    dc_list_dict[row['dc_id']] = [host_list, dc_attributes, dc_power_traces, vm_allocation_policy]
                host_id_start[row['dc_id']] += len(host_list)
            for key, value in dc_list_dict.items():
                dc_list.append(
                    PowerDatacenter(key, value[1], value[2], value[3], value[0]))
    except Exception as err:
        logging.error(f'Unable to import datacenters from file. Unexpected {err=}, {type(err)=}')
        raise Exception(f'Unable to import datacenters from file. Unexpected {err=}, {type(err)=}')
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


def create_cloud(dc_list: list[PowerDatacenter]) -> Cloud:
    """Create a cloud from the list of data centers
    :param dc_list: list of datacenters
    :type dc_list: list[Datacenter]
    :return: cloud
    :rtype: Cloud
    """
    logging.info(f'Creating the cloud.')
    cloud_attributes = {'cloud_id': 1}
    match conf.dc_selection_policy:
        case 'FirstFit':
            dc_selection_policy = DCSelectionPolicyFirstFit(dc_list)
        case 'RoundRobin':
            dc_selection_policy = DCSelectionPolicyRoundRobin(dc_list)
        case default:
            raise ValueError('dc selection policy not implemented')
    return Cloud(cloud_attributes, dc_list, dc_selection_policy)


if __name__ == '__main__':
    if conf.enable_log:
        enable_logging(conf.vm_file.replace('csv', 'log'))
        logging.info(f'Initializing PyCloudSim...')

    # 1) Create Datacenter(s) and Cloud
    datacenters = create_datacenter_from_file(conf.dc_file, conf.pue_file, conf.br_cost_file, conf.solar_file)
    cloud = create_cloud(datacenters)

    # 2) Create VM(s) either manually or from a file
    vms = create_vms_from_file(conf.vm_file)
    # vms = create_vms()

    # 3) Create a Broker and submit VMs to it
    broker = create_broker(cloud)
    broker.submit_vm_list(vms)
    cloud.set_broker(broker)

    # 4) Create and initialize simulation environment and event processors
    sim_time = conf.sim_time
    sim = PyCloudSim(sim_time, broker, cloud, vms)

    # 5) Start the simulation
    sim.start_simulation()

    # 5) Stop the simulation and finalize Results
    sim.stop_simulation()

    # 6) Plot the results
    power_readings, num_vms, num_rejected = parse(conf.vm_file.replace('csv', 'log'))
    plot_results(power_readings, num_vms, num_rejected)

