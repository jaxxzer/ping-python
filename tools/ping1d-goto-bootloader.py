#!/usr/bin/env python

#simplePingExample.py
from brping import Ping1D, definitions
import time
import argparse

from builtins import input

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
# parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
# parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate. E.g: 115200")
# parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9090")
# args = parser.parse_args()
# if args.device is None and args.udp is None:
#     parser.print_help()
#     exit(1)

# Make a new Ping
myPing = Ping1D()
# if args.device is not None:
    # myPing.connect_serial(args.device, args.baudrate)
myPing.connect_serial("/dev/ttyUSB0", 2000000)
# elif args.udp is not None:
#     (host, port) = args.udp.split(':')
#     myPing.connect_udp(host, int(port))

myPing.control_goto_bootloader()
print(myPing.wait_message([definitions.COMMON_ACK, definitions.COMMON_NACK]))
