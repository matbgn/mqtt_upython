import config
import math
from time import sleep

from machine import Pin, Signal, PWM, unique_id

import binascii
import random

from umqttsimple import MQTTClient

try:
    import ujson as json
except:
    import json

# These defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {
    "client_id": b"esp8266_" + binascii.hexlify(unique_id()),
    "topic": b"home",
}

global led_pin


def setup_pins():
    global led_pin

    led_pin = Pin(2, Pin.OUT, value=0)

    led = Signal(led_pin, invert=True)

    for i in range(3):
        print("Led ON")
        led.on()
        print(led.value())
        sleep(1)
        print("Led OFF")
        led.off()
        print(led.value())
        sleep(1)


def pulse(iPwm, t):
    for i in range(20):
        iPwm.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        sleep(t / 1000)


def load_config():
    try:
        with open("/config.json") as f:
            config = json.loads(f.read())
    except (OSError, ValueError):
        print("Couldn't load /config.json")
        save_config()
    else:
        CONFIG.update(config)
        print("Loaded config from /config.json")


def save_config():
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(CONFIG))
    except OSError:
        print("Couldn't save /config.json")


def main():
    global led_pin
    led_pulse = PWM(led_pin, freq=1000)

    client = MQTTClient(CONFIG['client_id'], server=config.MQTT_BROKER,
                        user=config.MQTT_USER, password=config.MQTT_PASSWD)
    client.connect()
    print("Connected to MQTT Broker {}".format(config.MQTT_BROKER))
    while True:
        # data = sensor_pin.value()
        data = int(random.getrandbits(6))
        client.publish('{}/{}'.format(CONFIG['topic'],
                                      CONFIG['client_id']),
                       bytes(str(data), 'utf-8'))
        print('Sensor state: {}'.format(data))
        pulse(led_pulse, 50)
        sleep(5)


if __name__ == '__main__':
    setup_pins()
    load_config()
    setup_pins()
    main()
