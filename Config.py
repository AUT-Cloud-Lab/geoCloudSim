class Config:
    # simulator
    sim_time = 10000
    enable_log = True
    verbose = False

    # broker

    # cloud
    dc_selection_policy = 'PPO'
    # num_dcs = 2  # number of datacenters

    # datacenter
    # num_hosts = 1  # number of hosts within each datacenter
    dc_file = 'csv/dcs.csv'
    pue_file = 'csv/pue.csv'
    br_cost_file = 'csv/br_cost.csv'
    solar_file = 'csv/solar_real.csv'
    dc_attributes = {'arch': 'x86', 'os': 'Linux', 'vmm': 'Xen', 'time_zone': 10.0,
                     'cost_per_mips': 3.0, 'cost_per_ram': 0.05, 'cost_per_storage': 0.001,
                     'cost_per_bw': 0.0}
    vm_allocation_policy = 'FirstFit'
    consolidation = True

    # host
    # mips = 1000  # host MIPS
    # ram = 2048  # host memory(MB)
    # bw = 100000  # host network bandwidth (MB/s)
    # storage = 1000000  # host storage (MB)
    # max_power = 195  # maximum power of host (sum of dynamic and static power at full utilization)
    # stat_power = 52  # static (idle) power of host (at zero utilization)
    # # power ratios (the contribution of each resource to total dynamic power of host)
    # mips_pr, ram_pr, bw_pr, storage_pr = 0.7, 0.26, 0.04, 0

    # workload
    # vm_file = 'csv/vms_HighDuration_1.csv'
    vm_file = 'csv/vms_test.csv'

    # miscellaneous
    eps = 1e-3

    # RL
    penalty = 10000
    discount = 0.5
    learn_rate = 3e-4
    num_epi = 200
    batch_size = 32
    memory = 10000
    horizon = 20
