#!/usr/bin/env python

from brping import PingDevice, definitions, pingmessage
import time
import argparse

import numpy as np
import matplotlib.pyplot as plt

from builtins import input
BPRX_PORT = 12000
BPTX_PORT = 12001

##Parse Command line options
############################
parser = argparse.ArgumentParser(description="beamplot control")
parser.add_argument('--host', action="store", required=True, type=str, help="beamplot machine ip address")
parser.add_argument('--rx', action="store", required=False, type=int, default=12000, help="beamplot rx device udp port")
parser.add_argument('--tx', action="store", required=False, type=int, default=12001, help="beamplot tx device udp port")
args = parser.parse_args()

# Make a new Ping
bprx = PingDevice()
bptx = PingDevice()

bprx.connect_udp(args.host, args.rx)
bptx.connect_udp(args.host, args.tx)

if bprx.initialize() is False:
    print("Failed to initialize beamplot rx!")
    exit(1)

if bptx.initialize() is False:
    print("Failed to initialize beamplot tx!")
    exit(1)

m = pingmessage.PingMessage(definitions.BEAMPLOT_TAKE_SAMPLES)
m.nsamples = 100
m.tx_frequency = 115000
m.tx_periods = 10
m.opamp1 = 1
m.opamp2 = 1
m.adc_sample_time = 4
m.fs = 1000000
m.pack_msg_data()
bprx.write(m.msg_data)
bptx.write(m.msg_data)

rxResponse = bprx.wait_message([definitions.BEAMPLOT_RX_DATA, definitions.COMMON_NACK], 1)
txResponse = bptx.wait_message([definitions.BEAMPLOT_RX_DATA, definitions.COMMON_NACK], 1)

data = np.frombuffer(rxResponse.data, dtype=np.uint8)

plt.plot(data)
plt.show()