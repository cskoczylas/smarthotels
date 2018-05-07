# Usage

To start, set up the Raspberry Pi as a wireless access point. For instructions on how to do so, check out [this guide on Raspberry Pi's site](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)
Afterwards, connect the bulbs to the Pi's access point using the TP-Link KASA app on Android or iPhone [Currently working on a way to bypass this part]. Once connected to the AP, you import `smartbulb.py` into your file using 
```
from smartbulb import SmartBulb
```
From there, you can add a lightbulb using 
```
bulb = SmartBulb("XXX.XXX.XXX.XXX")
```
with `XXX.XXX.XXX.XXX` being the lightbulb's IP address. You can use `discover.py` to find all IP addresses of any smart bulbs on the local network. 
```
from discover import Discover

for dev in Discover.discover():
	print(dev)
```
Once you have set up your bulb, you can control them using `bulb.state("X")`, where `X = "ON" | "OFF"`, and `bulb.brightness(Y)`, where `Y` is an integer from 0 to 100.
You can look at `test.py` for examples on how to use the libraries.
