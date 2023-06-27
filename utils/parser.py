import re
from csv import reader


def parse(log_file):
    with open(log_file) as log:
        lines = list(reader(log, ))
        power_readings = {}
        num_rejected = 0
        num_vms = {}
        rewards = []
        for line in lines:
            if line[0].find('Now consumes') != -1:
                dc_id = int(re.findall(r'[dc_id: ][\d]+', line[1])[1])
                if dc_id in power_readings.keys():
                    time_stamp = int(re.findall(r'\[\d+\]', line[0])[0].replace('[', '').replace(']', ''))
                    power_readings[dc_id][time_stamp] = float(re.findall(r'[Now consumes ][\d]+[.][\d]+', line[0])[0])
                    num_vms[dc_id][time_stamp] = int(re.findall(r'[and hosts ][\d]+', line[1])[0])
                else:
                    power_readings[dc_id] = dict()
                    num_vms[dc_id] = dict()
                    time_stamp = int(re.findall(r'\[\d+\]', line[0])[0].replace('[', '').replace(']', ''))
                    power_readings[dc_id][time_stamp] = float(re.findall(r'[Now consumes ][\d]+[.][\d]+', line[0])[0])
                    num_vms[dc_id][time_stamp] = int(re.findall(r'[and hosts ][\d]+', line[1])[0])
            if line[0].find('rejected') != -1:
                num_rejected += 1
            if line[0].find('reward =') != -1:
                if re.search(r'[reward = ][+-]?[\d]+[.][\d]+', line[0]):
                    rewards.append(float(re.findall(r'[reward = ][+-]?[\d]+[.][\d]+', line[0])[0]))
                else:
                    rewards.append(float(re.findall(r'[reward = ][+-]?[\d]+', line[0])[0]))

    return power_readings, num_vms, num_rejected, rewards

