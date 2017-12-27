#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Eric Dufresne
import logbook
import Python_DHT


class DHTSensorException(Exception):
    pass


class DHTSensorController(object):
    valid_sensor_types = [
        Python_DHT.DHT11, Python_DHT.DHT22, Python_DHT.AM2302
    ]
    _temperature = 0
    _humidity = 0.0

    def __init__(self, gpio_pin, sensor_type=Python_DHT.DHT22):
        self.validate_sensor_type(sensor_type)
        self.sensor_type = sensor_type
        self.gpio_pin = gpio_pin

    def validate_sensor_type(self, sensor_type):
        if sensor_type not in self.valid_sensor_types:
            raise DHTSensorException(
                "Unknown sensor type."
            )

    def read(self):
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        _humidity, _temperature = Python_DHT.read_retry(self.sensor_type, self.gpio_pin)
        if _humidity is not None and _temperature is not None:
            self._temperature = _temperature
            self._humidity = float(_humidity)
            logbook.debug("temperature: {0}; humidity: {1}".format(self._temperature, self._humidity))
            return True
        else:
            raise DHTSensorException(
                'Read failed.'
            )

    @property
    def temperature(self):
        self.read()
        return round(self._temperature, 1)

    @property
    def humidity(self):
        self.read()
        return int(round(self._humidity, 0))

    def __repr__(self):
        return "DHT: {0}°C, {1}% RH".format(
            self.temperature,
            self.humidity
        )
