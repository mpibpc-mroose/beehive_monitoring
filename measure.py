import datetime
import json
import pytz
import time

import logbook
import os
import requests
from RPi.GPIO import cleanup

from lib.scale import BeeHiveScale
from lib.dht import DHTSensorController
import settings

secrets = json.load(
    open(
        os.path.join(
            os.path.dirname(__name__),
            "secrets.json"
        ),
        "r"
    )
)
mail_log_settings = secrets["logging"]

logger = logbook.NestedSetup([
    logbook.NullHandler(),
    logbook.SyslogHandler(
        level=logbook.INFO
    ),
    logbook.MailHandler(
        from_addr=mail_log_settings["sender"],
        recipients=mail_log_settings["recipients"],
        level=logbook.ERROR,
        credentials=(
            mail_log_settings["username"],
            mail_log_settings["password"]
        ),
        server_addr=(
            mail_log_settings["server"],
            mail_log_settings["port"]
        ),
        secure=mail_log_settings["secure"],
        bubble=True
    )
])


def acquire_weights(
        scale_obj, sleep_time=settings.WEIGHT_MEASURE_WAIT_TIME, measure_count=settings.WEIGHT_MEASURE_COUNT
):
    """
    to ensure accuracy of the weight do a number of
    measures with sleep time in between

    :param scale_obj: BeeHiveScale object
    :type scale_obj: BeeHiveScale
    :param sleep_time: how long to wait between measures
    :type sleep_time: float
    :param measure_count: umber of measures
    :type measure_count: int
    :return: list of measures
    :rtype list
    """
    logbook.info("start acquire weights")
    _measures = []
    for count in range(measure_count + 1):
        weight = scale_obj.weight
        logbook.info("weight: {weight} kg".format(weight=weight))
        _measures.append(scale_obj.weight)
        if count < measure_count:
            logbook.debug("wait for {0}s".format(sleep_time))
            time.sleep(sleep_time)
    return _measures


def read_to_json(scale, dht):
    """
    acquire measures and return them as a json serialized string

    :param scale: BeeHiveScale object
    :type scale: BeeHiveScale
    :param dht: DHTSensorController object
    :type dht: DHTSensorController
    :return: json result
    :rtype str
    """
    _temperature = dht.temperature
    _humidity = dht.humidity
    logbook.info("DHT: {0}°C and {1}%rF".format(_temperature, _humidity))
    return json.dumps({
        "timestamp": datetime.datetime.now(pytz.timezone('Europe/Berlin')).isoformat(),
        "weight": {
            "value": acquire_weights(scale_obj=scale),
            "unit": "kg"
        },

        "temperature": {
            "value": _temperature,
            "unit": "°C"
        },
        "humidity": {
            "value": _humidity,
            "unit": "%"
        }
    })


def send_to_server(data):
    token = secrets["token"]
    response = requests.post(
        url=secrets["collector_url"],
        data={
            "token": token,
            "data": data
        }
    )
    if response.status_code != 200:
        raise Exception("data submission was not successfull: status code {code}".format(
            code=response.status_code
        ))


if __name__ == "__main__":
    with logger.applicationbound():
        with logbook.catch_exceptions():
            try:
                scale = BeeHiveScale(
                    offset=settings.OFFSET,
                    slope=settings.SLOPE
                )
                dht = DHTSensorController(
                    gpio_pin=17
                )
                send_to_server(data=read_to_json(scale=scale, dht=dht))
            finally:
                cleanup()
