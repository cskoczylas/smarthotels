#!/usr/bin/env python3

import time
from discover import Discover
from smartbulb import SmartBulb

"""
This is a test file to show how things work.
First it discovers all the bulbs on the local
network, then turns them all on, plays with 
brightness, then turns them off.
"""

lightbulbs = []

for dev in Discover.discover():
    lightbulbs.append(SmartBulb(dev))

for bulb in lightbulbs:
    bulb.state("ON")

time.sleep(3)

for bulb in lightbulbs:
    bulb.brightness(10)

time.sleep(3)

for bulb in lightbulbs:
    bulb.brightness(100)
    bulb.state("OFF")
