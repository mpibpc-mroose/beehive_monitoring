from statistics import median

import logbook
from hx711 import HX711


class BeeHiveScale(HX711):

    def __init__(self, slope=1, offset=0, dout_pin=5, pd_sck_pin=6, measure_count=25):
        super(BeeHiveScale, self).__init__(dout_pin=dout_pin, pd_sck_pin=pd_sck_pin, gain=128, channel='A')
        self.slope=slope
        self.offset=offset
        self.measure_count = measure_count

    def _measure(self):
        raw_value = median(self.get_raw_data(times=self.measure_count))
        logbook.debug("raw value: {0}".format(raw_value))
        return (raw_value - self.offset) / self.slope

    @property
    def weight(self):
        return round(self._measure(), 1)
