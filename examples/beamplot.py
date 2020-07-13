#!/usr/bin/env python

from brping import PingDevice, definitions, pingmessage
import time
import argparse

from tic import TicUdp

import numpy as np
import matplotlib.pyplot as plt

BPRX_PORT = 12000
BPTX_PORT = 12001
TIC_PORT = 12002
SAMPLES_PER_STEP = 10
STEPS = 10

##Parse Command line options
############################
parser = argparse.ArgumentParser(description="beamplot control")
parser.add_argument('--host', action="store", required=True, type=str, help="beamplot machine ip address")
parser.add_argument('--rx', action="store", required=False, type=int, default=BPRX_PORT, help="beamplot rx device udp port")
parser.add_argument('--tx', action="store", required=False, type=int, default=BPTX_PORT, help="beamplot tx device udp port")
parser.add_argument('--tic', action="store", required=False, type=int, default=TIC_PORT, help="tic stepper driver device udp port")
args = parser.parse_args()

# connect to the pings
bprx = PingDevice()
bptx = PingDevice()
bprx.connect_udp(args.host, args.rx)
bptx.connect_udp(args.host, args.tx)

# we need to write to this before we can read (haven't looked into it, something with udp recv)
# this will fail because the bptx rx uart line is disconnected (it's hooked to bprx)
bptx.initialize()

if bprx.initialize() is False:
    print("Failed to initialize beamplot rx!")
    exit(1)

# we will read the response from writing to the rxping
if bptx.initialize() is False:
    print("Failed to initialize beamplot tx!")
    exit(1)

# connect to the tic
tic = TicUdp(args.host, args.tic)

m = pingmessage.PingMessage(definitions.BEAMPLOT_TAKE_SAMPLES)
m.nsamples = 2000
m.tx_frequency = 115000
m.tx_periods = 5
m.opamp1 = 2
m.opamp2 = 1
m.adc_sample_time = 0
m.fs = 3000000
m.pack_msg_data()

plt.ion()
allavg = []
allstd = []
allmax = []
allmin = []
for step in range(STEPS):
    plt.figure(1)
    maxes = []
    for i in range(SAMPLES_PER_STEP):
        # this writes to both units
        bprx.write(m.msg_data)

        # and both units respond
        rxResponse = bprx.wait_message([definitions.BEAMPLOT_RX_DATA, definitions.COMMON_NACK], 1)
        txResponse = bptx.wait_message([definitions.BEAMPLOT_RX_DATA, definitions.COMMON_NACK], 1)

        data = np.frombuffer(rxResponse.data, dtype=np.uint8)
        thismax = np.amax(data)
        maxes.append(thismax)
        plt.clf()
        plt.plot(data)
        plt.draw()
        plt.pause(0.001)


    avg = np.mean(maxes)
    allavg.append(avg)
    std = np.std(maxes)
    allstd.append(std)
    max = np.amax(maxes)
    allmax.append(max)
    min = np.amin(maxes)
    allmin.append(min)

    print("STEP: %d avg: %d stddev: %d max: %d min: %d" % (step, avg, std, max, min))
    plt.figure(2)
    plt.clf()

    ax = plt.subplot(111, projection='polar')
    theta = np.arange(0, step+1, 1) * (2*np.pi)/(STEPS)
    ax.plot(theta, allmax)
    ax.set_rmax(300)

    plt.draw()
    plt.pause(0.001)

plt.ioff()
plt.show()
