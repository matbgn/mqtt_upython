import random

import esp
import gc
import network
import time
from machine import unique_id

try:
    import ubinascii as binascii
except:
    import binascii

try:
    import usocket as socket
except:
    import socket

try:
    import ure as re
except:
    import re

try:
    import ujson as json
except:
    import json

esp.osdebug(None)
gc.enable()
CONTENT = open('index.html', 'r').read()

# These defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {
    "captive_portal_ssid_name": b"ESP PORTAL " + binascii.hexlify(unique_id())
                                + b"_b" + str(random.getrandbits(16)).encode(),
    "network_name": "TO_BE_RETRIEVED_BY_CAPTIVE_PORTAL",
    "network_password": "TO_BE_RETRIEVED_BY_CAPTIVE_PORTAL",
    "client_id": b"esp8266_" + binascii.hexlify(unique_id())
}


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


def connection(network_name, network_password):
    attempts = 0
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print("Connecting to network...")
        station.active(True)
        station.connect(network_name, network_password)
        while not station.isconnected():
            print("Attempts: {}".format(attempts))
            attempts += 1
            time.sleep(5)
            if attempts > 3:
                return False
                break
    print('Network Config:', station.ifconfig())
    return True


class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.domain = ''

        m = data[2]
        tipo = (m >> 3) & 15
        if tipo == 0:
            ini = 12
            lon = data[ini]
            while lon != 0:
                self.domain += data[ini + 1:ini + lon + 1].decode("utf-8") + "."
                ini += lon + 1
                lon = data[ini]

    def response(self, ip):
        packet = b''
        print("Response {} == {}".format(self.domain, ip))
        if self.domain:
            packet += self.data[:2] + b"\x81\x80"
            packet += self.data[4:6] + b"\x00\x00\x00\x00"
            packet += self.data[12:]
            packet += b"\xc0\x0c"
            packet += b"\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04"
            packet += bytes(map(int, ip.split(".")))
        return packet


def captive_portal(essid_name):
    existing_config = False
    try:
        load_config()

        con = connection(CONFIG['network_name'], CONFIG['network_password'])
        if con is True:
            existing_config = True
            print("Network connected")
            ap = network.WLAN(network.AP_IF)
            ap.active(False)  # turn off AP SSID
        else:
            existing_config = False
            print("Incorrect network configuration")
    except:
        print("No saved network")

    if existing_config is False:
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=essid_name, authmode=1)
        ip = ap.ifconfig()[0]
        print("DNS Server: dom.query. 60 in A {:s}".format(ip))
        print("Server SSID: {:s}".format(essid_name))

        udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udps.setblocking(False)
        udps.bind(('', 53))

        s = socket.socket()
        ai = socket.getaddrinfo(ip, 80)
        print("Web Server: Bind address information: ", ai)
        addr = ai[0][-1]

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        s.settimeout(2)
        print("Web Server: Listening http://{}:80/".format(ip))

        regex = re.compile("ssid=(.*?)&password=(.*?)$")

        set_connection = False
        while set_connection is False:
            try:
                data, addr = udps.recvfrom(4096)
                print("Incoming data...")
                DNS = DNSQuery(data)
                udps.sendto(DNS.response(ip), addr)
                print("Replying: {:s} -> {:s}".format(DNS.domain, ip))
            except:
                print("No DNS Client")

            try:
                res = s.accept()
                client_sock = res[0]
                client_addr = res[1]

                req = client_sock.recv(4096)
                print("Request:")
                print(req)
                client_sock.send(CONTENT)
                client_sock.close()
                print()
                search_result = regex.search(req)
                if search_result:
                    incoming_network_name = search_result.group(1)
                    incoming_network_pass = search_result.group(2)
                    con = connection(incoming_network_name, incoming_network_pass)
                    if con is True:
                        CONFIG['network_name'] = incoming_network_name
                        CONFIG['network_password'] = incoming_network_pass
                        save_config()
                        set_connection = True


            except:
                print("Timeout")
            time.sleep_ms(1000)
        udps.close()


def main():
    captive_portal(CONFIG['captive_portal_ssid_name'])


main()
