import re
from csv import reader


def parse(log_file):
    with open(log_file) as log:
        lines = list(reader(log, ))
        power_readings = {}
        num_rejected = 0
        num_vms = {}
        for line in lines:
            if line[1].find('Now consumes') != -1:
                dc_id = int(re.findall(r'[dc_id: ][\d]+', line[2])[1])
                if dc_id in power_readings.keys():
                    time_stamp = int(re.findall(r'\[\d+\]', line[1])[0].replace('[', '').replace(']', ''))
                    power_readings[dc_id][time_stamp] = float(re.findall(r'[Now consumes ][\d]+[.][\d]+', line[1])[0])
                    num_vms[dc_id][time_stamp] = int(re.findall(r'[and hosts ][\d]+', line[2])[0])
                else:
                    power_readings[dc_id] = dict()
                    num_vms[dc_id] = dict()
                    time_stamp = int(re.findall(r'\[\d+\]', line[1])[0].replace('[', '').replace(']', ''))
                    power_readings[dc_id][time_stamp] = float(re.findall(r'[Now consumes ][\d]+[.][\d]+', line[1])[0])
                    num_vms[dc_id][time_stamp] = int(re.findall(r'[and hosts ][\d]+', line[2])[0])

            if line[1].find('rejected') != -1:
                num_rejected += 1

    return power_readings, num_vms, num_rejected

