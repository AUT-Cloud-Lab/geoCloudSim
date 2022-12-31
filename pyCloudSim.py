# This is pyCloudSim class, which is used to initialize, start and stop the simulator
# @author Mahmoud Momtazpour

class PyCloudSim(object):
    simTime = 100

    def __init__(self, time=None):
        if time is not None:
            if isinstance(time, int) and time > 0:
                self.simTime = time
            else:
                print('The value should be a positive integer, default value of 100 will be used.')

    def initialize(self, time):
        if isinstance(time, int) and time > 0:
            self.simTime = time
        else:
            print('The value should be a positive integer, default value of 100 will be used.')

    def get_time(self):
        return self.simTime
