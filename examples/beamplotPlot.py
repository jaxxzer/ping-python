#!/usr/bin/env python

from brping import PingDevice, definitions, pingmessage
import numpy as np
import matplotlib.pyplot as plt

import time
import argparse


##Parse Command line options
############################
parser = argparse.ArgumentParser(description="beamplot control")
parser.add_argument('--tx', action="store", required=True, type=str, help="beamplot tx device port. E.g: /dev/ttyUSB0")
parser.add_argument('--rx', action="store", required=True, type=str, help="beamplot rx device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=3000000, help="Ping device baudrate. E.g: 115200")
args = parser.parse_args()

# Make a new Ping
bprx = PingDevice()
bptx = PingDevice()

bprx.connect_serial(args.rx, args.baudrate)
bptx.connect_serial(args.tx, args.baudrate)

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
