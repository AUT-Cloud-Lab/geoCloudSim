# This is pyCloudSim, a cloud simulator written in Python.
# It is developed and maintained by M. Momtazpour

from PyCloudSim import PyCloudSim
from Host import Host
from RamProvisioner import RamProvisioner
from BwProvisioner import BwProvisioner
from MipsProvisioner import MipsProvisioner
from StorageProvisioner import StorageProvisioner
from VMAllocationPolicyLeastMips import VMAllocationPolicyLeastMips
from VMCloudAllocationPolicy import VMCloudAllocationPolicy
from Datacenter import Datacenter
from Broker import Broker
from Cloud import Cloud
from VM import VM
from csv import DictReader


def create_vms():
    vm_list = []
    num_vms = 2

    # adding some homogeneous VMs
    mips = 100  # host MIPS
    ram = 256  # host memory(MB)
    storage = 100000  # host storage (MB)
    bw = 1000  # host network bandwidth (MB/s)
    vmm = "Xen"  # Virtual Machine Monitor
    user_id = 1  # same user ID for all VMs
    for vm_id in range(num_vms):
        vm_list.append(VM(vm_id, user_id, mips, ram, bw, storage, vmm))
    return vm_list

def create_vms_from_file():
    vm_list = []
    with open('vms.csv', mode='r') as vm_file:
        vm_dict = DictReader(vm_file)
        for row in vm_dict:
            vm_list.append(VM(row['vm_id'], row['user_id'], float(row['mips']), float(row['ram']), float(row['bw']),
                              float(row['storage']), row['vmm'], float(row['arrival_time']), float(row['duration'])))
    return vm_list

def create_datacenter():
    host_list = []
    dc_list = []
    num_hosts = 1
    num_dcs = 1

    # adding some homogeneous hosts
    mips = 1000  # host MIPS
    ram = 2048  # host memory(MB)
    storage = 1000000  # host storage (MB)
    bw = 10000000  # host network bandwidth (MB/s)
    ram_provisioner = RamProvisioner(ram)
    mips_provisioner = MipsProvisioner(mips)
    storage_provisioner = StorageProvisioner(storage)
    bw_provisioner = BwProvisioner(bw)
    for host_id in range(num_hosts):
        host_list.append(Host(host_id, ram_provisioner, bw_provisioner, storage_provisioner, mips_provisioner))
    datacenter_attributes = {'arch': 'x86', 'os': 'Linux', 'vmm': 'Xen', 'time_zone': 10.0,
                             'cost_per_mips': 3.0, 'cost_per_ram': 0.05, 'cost_per_storage': 0.001, 'cost_per_bw': 0.0}
    vm_allocation_policy = VMAllocationPolicyLeastMips(host_list)
    scheduling_interval = 0
    for dc_id in range(num_dcs):
        dc_list.append(Datacenter(dc_id, datacenter_attributes, vm_allocation_policy, scheduling_interval, host_list))
    return dc_list


def create_broker(cloud):
    return Broker(cloud)


def create_cloud(dc_list):
    cloud_attributes = {'name': 'my_cloud', 'cloud_id': 1}
    vm_cloud_allocation_policy = VMCloudAllocationPolicy(dc_list)
    return Cloud(cloud_attributes, dc_list, vm_cloud_allocation_policy)


def print_hi():
    print(f'Welcome to pyCloudSim')


if __name__ == '__main__':
    print_hi()

    # 1) Create Datacenter(s) and Cloud
    datacenters = create_datacenter()
    cloud = create_cloud(datacenters)

    # 2) Create VM(s)
    vms = create_vms_from_file()

    # 3) Create a Broker and submit VMs to it
    broker = create_broker(cloud)
    broker.submit_vm_list(vms)

    # 4) Create and Initialize Simulation environment and processes
    sim_time = 10000
    sim = PyCloudSim(sim_time, broker, datacenters, vms)

    # 5) Initialize and Start the simulation
    sim.start_simulation()

    # 5) Finalize Results
    sim.stop_simulation()
