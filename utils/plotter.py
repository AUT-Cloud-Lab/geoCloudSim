from matplotlib import pyplot as plt
from Config import Config as conf


def plot_results(power_readings, num_vms, num_rejected, rewards=None):
    for dc_id, pr in power_readings.items():
        plt.plot(pr.keys(), pr.values())
        plt.title(f'dc selection: {conf.dc_selection_policy}')
    plt.show()

    plt.figure()
    for dc_id, nv in num_vms.items():
        plt.plot(nv.keys(), nv.values())
    plt.show()

    print(num_rejected)

    if rewards is not None:
        plt.figure()
        plt.plot(rewards)
        plt.show()
