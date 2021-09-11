import config
from boot import CONFIG
import math
from time import sleep
import random

from machine import Pin, Signal, PWM

from umqttsimple import MQTTClient

try:
    import ujson as json
except:
    import json

import webrepl


global led_pin

TOPIC = b'home'


def setup_webrepl():
    try:
        with open("webrepl_cfg.py", "w") as f:
            f.write(CONFIG['webrepl_password'])
            webrepl.start()
    except OSError:
        print("Couldn't initiate WebREPL")


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
        client.publish('{}/{}'.format(TOPIC,
                                      CONFIG['client_id']),
                       bytes(str(data), 'utf-8'))
        print('Sensor state: {}'.format(data))
        pulse(led_pulse, 50)
        sleep(5)


if __name__ == '__main__':
    setup_webrepl()
    setup_pins()
    main()
