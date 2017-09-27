import argparse
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

config.ver = input("version > ")
#config.face_or_words = input("moment(face) or succession(words) > ")
#face_or_wordsはconfigつきとなしがある

def serial_loop():
    with serial.Serial('COM5', 9600, timeout=0.1) as ser:
        between_a_and_a = False
        want_predict_num_array_raw = []
        arranged_sensor_date_list = []
        count_label = 0
        machine = svm.setup()
        try:
            while True:
                s = ser.readline()
                m = None
                try:
                    de = s.decode('utf-8')
                    m = re.match("\-*[\w]+", str(de))
                except Exception as e:
                    pass
                if(m != None):
                    num = m.group()
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
                        svm.stream_w_face(machine, np.array(arranged_sensor_date_list).astype(np.int64))
                else:
                    pass
        except:
             print("Unexpected error:", sys.exc_info()[0])
             raise
        ser.close()

ser_loop = threading.Thread(target=serial_loop,name="ser_loop",args=())
ser_loop.setDaemon(True)
ser_loop.start()

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
