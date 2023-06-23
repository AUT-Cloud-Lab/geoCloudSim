import logging


def enable_logging():
    """Enable logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)10s]: %(message)6s',
        filename='simulation.log', filemode="w")  # pass explicit filename here
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Logging enabled')


def log_me(kind, time, sender, message, vm_id=None, dc_id=None, host_id=None):
    msg = f'[{time}]'.ljust(8) + f'[{sender}]'.ljust(15) + f'[{message}]'.ljust(50) + (f'[vm_id:{vm_id}]' if vm_id is not None else '').ljust(15) + (
        f'[dc_id: {dc_id}]' if dc_id is not None else '').ljust(15) + (
              f'[host_id: {host_id}]' if host_id is not None else '').ljust(15)
    if kind == 'INFO':
        logging.info(msg)
    if kind == 'WARN':
        logging.warning(msg)
    if kind == 'DEBUG':
        logging.debug(msg)
