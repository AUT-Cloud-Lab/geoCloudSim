import re
from csv import reader
from matplotlib import pyplot as plt
from Config import Config as conf

with open('log/vms_HighDuration_1.log') as log:
    lines = list(reader(log,))
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


for dc_id, pr in power_readings.items():
    plt.plot(pr.keys(), pr.values())
    plt.title(f'dc selection: {conf.dc_selection_policy}')
plt.show()

plt.figure()
for dc_id, nv in num_vms.items():
    plt.plot(nv.keys(), nv.values())
plt.show()

print(num_rejected)

