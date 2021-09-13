<h1 align="center">Esp8266 MQTT Client based on MicroPython</h1>

<p align="center">
  <img width="200" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Micropython-logo.svg/2000px-Micropython-logo.svg.png" />
</p>
<p align="center">How to start coding with esp8266 (Wemos D1 mini) on micropython</p>
<p align="center">
  <a href="https://github.com/matbgn/mqtt_upython/blob/master/docs/LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"/></a>
  <a href="https://github.com/matbgn/mqtt_upython/pull/new"><img src="https://img.shields.io/badge/PRs%20-welcome-brightgreen.svg" alt="PRs Welcome" /></a>
</p>

<div align="center">
    <table border="0">
      <tr>
        <td>:bulb:</td>
        <td>For a convinient interactive documentation please visit: <a href="https://matbgn.github.io/mqtt_upython/">https://matbgn.github.io/mqtt_upython/</a></td>
      </tr>
    </table>
</div>

## Introduction
This repository is aimed to guide you through the complete process to work with [MicroPython](https://micropython.org/) on ESP8266 especially Wemos D1 mini.

All contributions are welcomed!

## How to start


## Documentation


## BOM (Bill Of Material)
| Qty | Description                                                       | Price |
|-----|-------------------------------------------------------------------|-------|
| 1   | [Wemos D1 Mini](https://www.aliexpress.com/item/32651747570.html) | ~2$   |
|     |                                                                   |       |
|     |                                                                   |       |

## Config file (config.py)

    WIFI_SSID = 'YOUR_WIFI_SSID_NAME'
    WIFI_PASSWD = 'YOUR_WIFI_PASSWORD'
    MQTT_BROKER = 'YOUR_MQTT_BROKER_IP_ADRESS'
    MQTT_USER = 'MQTT_USER_FOR_CONNECTION'
    MQTT_PASSWD = 'MQTT_PASS_FOR_CONNECTION'

## Captive portal
![Captive portal](img/portal.png)

## Web editor
![Web editor](img/webrepl.png)