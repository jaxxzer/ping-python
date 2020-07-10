#!/usr/bin/env python

from brping import PingDevice, definitions, pingmessage
import argparse

##Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping python library example.")
parser.add_argument('--host', action="store", required=True, type=str, help="beamplot machine ip address")
parser.add_argument('--rx', action="store", required=False, type=int, default=12000, help="beamplot rx device udp port")
args = parser.parse_args()
if args.host is None:
    parser.print_help()
    exit(1)

# Make a new Ping
bp = PingDevice()
bp.connect_udp(args.host, args.rx)


if bp.initialize() is False:
    print("Failed to initialize beamplot!")
    exit(1)

bp.request(definitions.COMMON_DEVICE_INFORMATION)

if bp._device_type != 20:
    print("Device is not beamplot rx!")
    exit(1)

responseTimeout = 1

m = pingmessage.PingMessage(definitions.BEAMPLOT_TAKE_SAMPLES)
m.nsamples = 100
m.tx_frequency = 115000
m.tx_periods = 10
m.pack_msg_data()
bp.write(m.msg_data)

print(bp.wait_message([definitions.BEAMPLOT_RX_DATA, definitions.COMMON_NACK], responseTimeout))
