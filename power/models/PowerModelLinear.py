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
        if 0 <= mips_util <= 1 and 0 <= ram_util <= 1 and 0 <= bw_util <= 1 and 0 <= storage_util <= 1:
            return self._stat_p + (self._max_p - self._stat_p) * (mips_util * self._mips_p_r +
                                                                  ram_util * self._ram_p_r +
                                                                  bw_util * self._bw_p_r +
                                                                  storage_util * self._storage_p_r)
        else:
            raise ValueError('Utilization exceeds its boundaries [0,1]')
