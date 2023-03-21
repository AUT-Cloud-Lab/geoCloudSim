This is pyCloudSim, a cloud simulator written in Python. It is developed and maintained by Mahmoud Momtazpour. 

Inspired by CloudSim, pyCloudSim can be considered as a simplified (and a slightly different) version of it, written in Python. 

Currently, it only supports IaaS service (VM allocation in a cloud data center). 


Its basic features are:

1. Models data centers, hosts, and VMs. Cloudlets are not modeled in the current version.

2. Defines DC Selection Policies to selects a datacenter (in a geographically distributed datacenters setup) for an incoming VM request. 

3. Defines VM Allocation Policies to allocate VMs to hosts.

4. Defines Resource (MIPS, RAM, BW, Storage) Privisioners to provision requested resources on hosts to VMs.

To speedup the simulation, pyCloudSim uses SimPy v4.0.2, a discrete-event simulation framework. 



Usage:

A vms.csv file has been included as the workload, containing a number of VM requests. Each row is a VM request with its predefined characteristics (MIPS, RAM, BW, Storage, arrival time and duration).

The starting point is main.py, which sets up the simulation and starts it. The result of simulation is logged in simulation.log.