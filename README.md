# geoCloudSim, a Pythonic simulator for modeling and simulating geo-distributed cloud data centers

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)


This is geoCloudSim, a geographically distributed cloud simulator written in Python. It is developed and maintained by Mahmoud Momtazpour. 

Inspired by CloudSim, geoCloudSim can be considered as a simplified (and a slightly different) version of it that supports simulation of geographically distributed cloud and is written in Python. 

## Basic Features

1. Models data centers, hosts, and VMs. Cloudlets are not modeled in the current version.

2. Defines DC Selection Policies to selects a datacenter (in a geographically distributed datacenters setup) for an incoming VM request. 

3. Defines VM Allocation Policies to allocate VMs to hosts.

4. Defines Resource (MIPS, RAM, BW, Storage) Privisioners to provision requested resources on hosts to VMs.

5. Models renewable energy to simulate green cloud 

To speedup the simulation, geoCloudSim uses SimPy v4.0.2, a discrete-event simulation framework. 

## Limitations
Currently, it only supports IaaS service (VM allocation in a geo-distributed cloud data centers) with limited set of features described above. 

## How to Use

A vms.csv file has been included as the workload, containing a number of VM requests. Each row is a VM request with its predefined characteristics (MIPS, RAM, BW, Storage, arrival time and duration).

The starting point is main.py, which sets up the simulation and starts it. The result of simulation is logged in simulation.log.
