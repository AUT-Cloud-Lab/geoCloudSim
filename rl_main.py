"""
Title:          PyCloudSim
Description:    A Python-based Cloud Simulator
Author(s):      Mahmoud Momtazpour
Licence:        GPL - https://www.gnu.org/copyleft/gpl.html
Copyright (c) 2022-2023, Amirkabir University of Technology, Iran
"""

from utils.creator import *
from tensorforce import Agent
from utils.parser import parse
from utils.plotter import plot_results
from utils.logger import enable_logging, log
from PyCloudSim import PyCloudSim


def predictor(pue_file: str, br_cost_file: str, solar_file: str):
    try:
        with open(pue_file, mode='r') as pue_file, \
                open(br_cost_file, mode='r') as br_cost_file, open(solar_file, mode='r') as solar_file:
            pue_list = list(reader(pue_file))
            br_cost_list = list(reader(br_cost_file))
            solar_list = list(reader(solar_file))
            host_id_start = dict()
    except Exception as err:
        log('ERROR', 0, f'Unable to import from file. Unexpected {err=}, {type(err)=}')
        raise Exception(f'Unable to import from file. Unexpected {err=}, {type(err)=}')


def init_rl():
    # Instantiate a PPO agent
    agent = Agent.create(
        agent='ppo',
        # Automatically configured network
        states=dict(type="float", shape=(16,)),
        actions=dict(type="int", shape=(), num_values=4),
        max_episode_timesteps=10000,
        network='auto',
        # Optimization
        batch_size=conf.batch_size, update_frequency=2, learning_rate=conf.learn_rate, subsampling_fraction=0.3,
        optimization_steps=5,
        # Reward estimation
        likelihood_ratio_clipping=0.1, discount=conf.discount, estimate_terminal=False,
        # Critic
        critic_network='auto',
        critic_optimizer=dict(optimizer='adam', multi_step=10, learning_rate=conf.learn_rate),
        # Preprocessing
        preprocessing=None,
        # Exploration
        exploration=0.01, variable_noise=0.0,
        # Regularization
        l2_regularization=0.1, entropy_regularization=0.01,
        # TensorFlow etc
        name='agent', device=None, parallel_interactions=1, seed=None, execution=None, saver=None,
        summarizer=None, recorder=None
    )
    return agent


if __name__ == '__main__':

    # Initialize RL
    agent = init_rl()

    train_dc_file = 'csv/dcs_test.csv'
    train_vm_file = 'csv/vms_test.csv'
    eval_vm_file = 'csv/vms_HighDuration_1.csv'
    train_log_file = train_vm_file.replace('csv', 'log')
    eval_log_file = eval_vm_file.replace('csv', 'log')
    # Train for num_epi episodes
    for i in range(conf.num_epi):
        print(f'starting episode {i}')
        if conf.enable_log:
            enable_logging(train_log_file)
            log('INFO', 0, f'Initializing PyCloudSim...')

        # Initialize episode
        # 1) Create Datacenter(s) and Cloud
        datacenters = create_power_datacenter_from_file(train_dc_file, conf.pue_file, conf.br_cost_file, conf.solar_file)
        cloud = create_cloud(datacenters, agent, evaluation=False)

        # 2) Create VM(s) either manually or from a file
        vms = create_vms(train_vm_file)
        # vms = create_vms()

        # 3) Create a Broker and submit VMs to it
        broker = create_broker(cloud)
        broker.submit_vm_list(vms)
        cloud.set_broker(broker)

        # 4) Create and initialize simulation environment and event processors
        sim_time = conf.sim_time
        sim = PyCloudSim(sim_time, broker, cloud, vms)

        # 5) Start the simulation
        sim.start_simulation()

        # 5) Stop the simulation and finalize Results
        sim.stop_simulation()

    # 6) Plot the results
    power_readings, num_vms, num_rejected, rewards = parse(train_log_file)
    plot_results(power_readings, num_vms, num_rejected, agent.reward_buffers[0])

    # Run an episode for evaluation

    if conf.enable_log:
        enable_logging(eval_log_file)
        log('INFO', 0, f'Initializing PyCloudSim...')

    # 1) Create Datacenter(s) and Cloud
    datacenters = create_power_datacenter_from_file(conf.dc_file, conf.pue_file, conf.br_cost_file, conf.solar_file)
    cloud = create_cloud(datacenters, agent, evaluation=True)

    # 2) Create VM(s) either manually or from a file
    vms = create_vms(eval_vm_file)
    # vms = create_vms()

    # 3) Create a Broker and submit VMs to it
    broker = create_broker(cloud)
    broker.submit_vm_list(vms)
    cloud.set_broker(broker)

    # 4) Create and initialize simulation environment and event processors
    sim_time = conf.sim_time
    sim = PyCloudSim(sim_time, broker, cloud, vms)

    # 5) Start the simulation
    sim.start_simulation()

    # 5) Stop the simulation and finalize Results
    sim.stop_simulation()

    # 6) Plot the results
    power_readings, num_vms, num_rejected, rewards = parse(eval_log_file)
    plot_results(power_readings, num_vms, num_rejected, agent.reward_buffers[0])
