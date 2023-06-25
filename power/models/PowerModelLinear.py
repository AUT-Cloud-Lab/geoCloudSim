from Config import Config as conf
from power.models.PowerModel import PowerModel


class PowerModelLinear(PowerModel):
    def __init__(self, max_power, stat_power, mips_power_ratio, ram_power_ratio, bw_power_ratio, storage_power_ratio):
        super().__init__(max_power, stat_power)
        if (mips_power_ratio + ram_power_ratio + bw_power_ratio + storage_power_ratio) != 1:
            raise ValueError('The sum of power ratios must be one!')
        self._mips_p_r = mips_power_ratio
        self._ram_p_r = ram_power_ratio
        self._bw_p_r = bw_power_ratio
        self._storage_p_r = storage_power_ratio

    def get_power(self, mips_util, ram_util, bw_util, storage_util):
        if -conf.eps <= mips_util <= 1 + conf.eps and -conf.eps <= ram_util <= 1 + conf.eps and -conf.eps <= bw_util <= 1 + conf.eps and -conf.eps <= storage_util <= 1 + conf.eps:
            util = (mips_util * self._mips_p_r +
                    ram_util * self._ram_p_r +
                    bw_util * self._bw_p_r +
                    storage_util * self._storage_p_r)
            if conf.consolidation:
                return self._stat_p * int(util != 0) + (self._max_p - self._stat_p) * util
            else:
                return self._stat_p + (self._max_p - self._stat_p) * util
        else:
            raise ValueError('Utilization exceeds its boundaries [0,1]')
