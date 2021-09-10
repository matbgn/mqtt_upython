import config
import network
import esp
import gc

esp.osdebug(None)
gc.collect()

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(config.WIFI_SSID, config.WIFI_PASSWD)

while not station.isconnected():
    pass

print('Connection to SSID successful')
print(station.ifconfig())
