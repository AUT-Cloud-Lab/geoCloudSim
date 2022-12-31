# This is pyCloudSim, a cloud simulator written in Python.
# It is developed and maintained by M. Momtazpour

from PyCloudSim import PyCloudSim


def print_hi():
    print(f'Welcome to pyCloudSim')


if __name__ == '__main__':
    print_hi()
    simTime = 1000
    sim = PyCloudSim(simTime)
    print(sim.get_time())
