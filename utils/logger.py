import logging
from Config import Config as conf


def enable_logging(log_file):
    """Enable logging"""
    logging.basicConfig(
        force=True,
        level=logging.INFO,
        format='[%(levelname)8s]: %(message)6s',
        filename=log_file, filemode="w")  # pass explicit filename here
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info('Logging enabled')


def log_me(kind, time, sender, message, vm_id=None, dc_id=None, host_id=None):
    if conf.enable_log:
        msg = f'[{time}]'.ljust(8) + f'[{sender}]'.ljust(15) + f'[{message}]'.ljust(50) + (
            f'[vm_id:{vm_id}]' if vm_id is not None else '').ljust(15) + (
                  f'[dc_id: {dc_id}]' if dc_id is not None else '').ljust(15) + (
                  f'[host_id: {host_id}]' if host_id is not None else '').ljust(15)
        match kind:
            case 'STAT':
                logging.info(msg)
            case 'INFO':
                if conf.verbose:
                    logging.info(msg)
            case 'WARN':
                logging.warning(msg)
            case 'DEBUG':
                if conf.verbose:
                    logging.debug(msg)
            case 'ERROR':
                logging.error(msg)
            case _:
                logging.info(msg)


def log(kind, time, msg):
    if conf.enable_log:
        msg = f'[{time}]'.ljust(8) + msg
        match kind:
            case 'INFO':
                logging.info(msg),
            case 'WARN':
                logging.warning(msg),
            case 'DEBUG':
                logging.debug(msg),
            case 'ERROR':
                logging.error(msg)
            case _:
                logging.info(msg)

