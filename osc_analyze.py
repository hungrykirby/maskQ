import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

import math
import serial

import re
import threading
import sys

import numpy as np

import config

import NeighborAlgorithm as na
import SupportVectorMachine as svm
import Calibrate
import GridSearch as gd

#config.learner = input("learner > ")
config.stream = input("is stream > ")
config.ver = input("version > ")
#config.face_or_words = input("moment(face) or succession(words) > ")
#face_or_wordsはconfigつきとなしがある

def serial_loop():
    '''
    OSC
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=12345,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.UDPClient(args.ip, args.port)
    '''
    Serial
    '''
    with serial.Serial('COM5', 9600, timeout=0.1) as ser:

        setPortCount = 0

        between_a_and_a = False
        want_predict_num_array_raw = []
        arranged_sensor_date_list = []
        count_label = 0
        learner = None #このスコープのみで有効な学習器
        if config.learner == "svm":
            learner = svm
        else:
            learner = na
        machine = learner.setup()
        try:
            while True:
                s = ser.readline()
                m = None

                if setPortCount < 100:
                    print("waiting port now" + str(setPortCount))
                    ser.write(bytes(str(2), 'UTF-8'))

                try:
                    de = s.decode('utf-8')
                    m = re.match("\-*[\w]+", str(de))
                except Exception as e:
                    pass
                if(m != None):

                    setPortCount = setPortCount + 1
                    
                    num = m.group()
                    #print(want_predict_num_array)
                    if num == "a":
                        between_a_and_a = True
                        count_label = 0
                        want_predict_num_array_raw = []
                    elif between_a_and_a:
                        want_predict_num_array_raw.append(int(num))

                    if len(want_predict_num_array_raw) == config.sensor_nums:
                        count_label = 0
                        if config.calibration_numbers is not None:
                            want_predict_num_array = want_predict_num_array_raw - config.calibration_numbers
                        else:
                            want_predict_num_array = want_predict_num_array_raw
                        config.is_calibration = Calibrate.start_calibration(config.is_calibration, want_predict_num_array)
                        while len(arranged_sensor_date_list) > 1:
                            arranged_sensor_date_list.pop(0)
                        arranged_sensor_date_list.append(want_predict_num_array)
                        want_predict_num_array = []
                        between_a_and_a = False
                        ser.flushInput()
                        #print(arranged_sensor_date_list[0])
                        p_label = learner.stream(machine, np.array(arranged_sensor_date_list).astype(np.int64))

                        #print(type(p_label))
                        msg = osc_message_builder.OscMessageBuilder(address = "/emotion")
                        msg.add_arg(int(p_label))
                        #msg = osc_message_builder.OscMessageBuilder(address = "/raw")
                        for a in arranged_sensor_date_list[0]:
                            msg.add_arg(int(a))
                        msg = msg.build()
                        client.send(msg)
                else:
                    pass
                    #print(type(m))
        except:
             print("Unexpected error:", sys.exc_info()[0])
             raise
        ser.close()

if config.stream == "s":
    ser_loop = threading.Thread(target=serial_loop,name="ser_loop",args=())
    ser_loop.setDaemon(True)
    ser_loop.start()
elif config.stream == "t" and config.face_or_words == "words":
    for i in range(50,300):
        config.length_array = i
        print(i)
        if config.learner == "na":
            na.setup()
        elif config.learner == "svm":
            svm.setup()
elif config.stream == "g":
    gd.start()
else:
    if config.learner == "svm":
        learner = svm
    else:
        learner = na
    machine = learner.setup()

def main():
    while True:
        console_input = input()
        if console_input == "s":
            config.is_input_word = True
        elif console_input == "e":
            config.is_input_word = False
            config.finish_input_word = True
        elif console_input == "o":
            config.is_calibration = True
        elif console_input != config.console_input_number:
            config.console_input_number = console_input
            print("c =", config.console_input_number)
        else:
            print("else")


if __name__ == "__main__":
    main()
