# geoCloudSim, a Pythonic simulator for modeling and simulating geo-distributed cloud data centers

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)


This is geoCloudSim, a geographically distributed cloud simulator written in Python. It is developed and maintained by Mahmoud Momtazpour. 

Inspired by CloudSim, geoCloudSim can be considered as a simplified (and a slightly different) version of it that supports simulation of geographically distributed cloud and is written in Python. 

## Main Features

1. geoCloudSim is super fast, owing to its discrete-event nature! It uses SimPy as its underlying simulation framework.

2. It models data centers, hosts, and VMs. 

3. It defines DC Selection Policies to selects a datacenter for an incoming VM request (in a geographically distributed datacenters setup).

4. It defines VM Allocation Policies to allocate VMs to hosts.

5. It defines Resource Privisioners (MIPS, RAM, BW, Storage) to provision requested resources on hosts to VMs.

6. It models renewable energy to simulate green cloud. It also supports renewable-aware DC selection and allocation policies.  

## Requirements
To speedup the simulation, geoCloudSim uses SimPy v4.0.2, a discrete-event simulation framework. 

## Limitations
Currently, it only supports IaaS service (VM allocation in a geo-distributed cloud data centers) with limited set of features described above. Cloudlets are not modeled in the current version.

## How to Use
### Step 1: Install Python 3
Visit [Python's official website](https://www.python.org/downloads/) and download the latest version of Python 3. Follow the installation instructions for your operating system.

### Step 2: Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies. Here's how you can set one up:

```bash
# Install virtualenv if it's not installed
pip install virtualenv

# Navigate to your project directory
cd path/to/your/project

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS and Linux
source venv/bin/activate
```
### Step 3: Clone the Repository
Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/AUT-Cloud-Lab/geoCloudSim.git
```

### Step 4: Install Dependencies
Navigate to the cloned repository's directory and install the required dependencies:

cd geoCloudSim
pip install -r requirements.txt

### Step 5: Run the Simulator
Now you're ready to run the simulator. But before that, you need a workload!

A vms.csv file has been included as a sample workload, containing a number of VM requests. Each row is a VM request with its predefined characteristics:

- MIPS: CPU demand in terms of million instructions per second
- RAM: memory capacity in GB
- BW: network bandwidth in GB/s
- Storage: storage capacity in GB
- arrival time: arrival time of the request in unit time
- duration: duration of the request in unit time

The starting point is main.py, which sets up the simulation environment and starts the simulator. The result of the simulation is logged in simulation.log.

To run the simulation, execute the following command:
```bash
python main.py
```

