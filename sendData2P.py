import argparse
import math
from pythonosc import osc_message_builder
from pythonosc import udp_client
import re
import sys
import os
import glob

import numpy as np

import config

import DataSetup

foldername = input("foldername is > ")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=12345,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.UDPClient(args.ip, args.port)

    sensors, labels = DataSetup.make_arr(foldername)
    sensordata_at_label = [[] for n in range(max(labels) + 1)]
    for n, l in enumerate(labels):
        print(n, l, sensors[n])
        sensordata_at_label[l].append(sensors[n])

    sensor_values = {
        "ave":[],
        "max":[],
        "min":[],
        "std":[], #標準偏差
        "var":[] #分散
    }
    for n, s in enumerate(sensordata_at_label):
        ave = np.mean(s, axis=0)
        _max = np.max(s, axis=0)
        _min = np.min(s, axis=0)
        std = np.std(s, axis=0)
        var = np.var(s, axis=0)
        sensor_values["ave"].append(ave)
        sensor_values["max"].append(_max)
        sensor_values["min"].append(_min)
        sensor_values["std"].append(std)
        sensor_values["var"].append(var)

    print(sensor_values)
    #msg = osc_message_builder.OscMessageBuilder(address="/test")
    msg = osc_message_builder.OscMessageBuilder(address="/sensor_nums")
    msg.add_arg(config.sensor_nums)
    msg = msg.build()
    client.send(msg)

    msg = osc_message_builder.OscMessageBuilder(address="/faces")
    msg.add_arg(len(sensor_values["ave"]))
    msg = msg.build()
    client.send(msg)

    for s in sensor_values:
        msg = osc_message_builder.OscMessageBuilder(address="/" + s)
        for s1 in sensor_values[s]:
            #print("s1", s1)
            for s2 in s1:
                #print(s2)
                msg.add_arg(float(s2))
        msg = msg.build()
        client.send(msg)


if __name__ == "__main__":
    main()
