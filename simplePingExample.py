#!/usr/bin/python -u

#simplePingExample.py
from brping import Ping1D
from brping import PingMessage
import time
import argparse

from builtins import input

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--device', action="store", required=True, type=str, help="Ping device port.")
parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate.")
args = parser.parse_args()

#Make a new Ping
myPing = Ping1D(args.device, args.baudrate)

def init():
    if myPing.set_mode_auto(True) is None:
        return False
    if myPing.set_ping_enable(True) is None:
        return False
    if myPing.set_ping_interval(20) is None:
        return False
    return True

if init() is False:
    print("Failed to initialize Ping!")
    exit(1)

print("start log")
print(myPing)
# Read and print distance measurements with confidence
while True:
    data = myPing.request(1300)
    if data:
        print("[[[%f]]]%s" % (time.time(), data.msg_data))
    else:
        print("Failed to get distance data")
    time.sleep(0.01)
