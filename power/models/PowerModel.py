from abc import ABC, abstractmethod


class PowerModel(ABC):
    def __init__(self, max_power, stat_power):
        if stat_power > max_power:
            raise ValueError('Max power cannot be lower than static power')
        else:
            self._max_p = max_power
            self._stat_p = stat_power

    @abstractmethod
    def get_power(self, mips_util, ram_util, bw_util, storage_util):
        pass
