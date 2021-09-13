from boot import CONFIG
import math
from time import sleep

from machine import Pin, Signal, PWM

from lib.umqttsimple import MQTTClient

from lib.hcsr04 import HCSR04

try:
    import ujson as json
except:
    import json


LED_PIN = None
TOPIC = "home/oil_tank"
SENSOR = None


def setup_pins():
    global LED_PIN, SENSOR
    LED_PIN = Pin(2, Pin.OUT, value=0)
    led = Signal(LED_PIN, invert=True)

    SENSOR = HCSR04(trigger_pin=16, echo_pin=0)

    for i in range(3):
        print("Led ON")
        led.on()
        sleep(1)
        print("Led OFF")
        led.off()
        sleep(1)


def pulse(iPwm, t):
    for i in range(20):
        iPwm.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        sleep(t / 1000)


def main():
    global LED_PIN, SENSOR
    led_pulse = PWM(LED_PIN, freq=1000)

    client = MQTTClient(CONFIG['client_id'], server=CONFIG['mqtt_broker_ip'],
                        user=CONFIG['mqtt_user'], password=CONFIG['mqtt_password'])
    client.connect()
    print("Connected to MQTT Broker {}".format(CONFIG['mqtt_broker_ip']))
    print("Sensor ID: {}".format(CONFIG['client_id']))
    while True:
        data = SENSOR.distance_cm()
        client.publish('{}/{}'.format(TOPIC,
                                      CONFIG['client_id']),
                       bytes(str(data), 'utf-8'))
        print('Sensor state: {}'.format(data))
        pulse(led_pulse, 50)
        sleep(5)


if __name__ == '__main__':
    setup_pins()
    main()
