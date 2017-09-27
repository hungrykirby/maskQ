import numpy as np
from scipy import signal
from pylab import *
import os

import shutil

import config
import Calibrate

import arrange

class Face(arrange.Arrange):
    def __init__(self, mode, sensor_nums):
        arrange.Arrange.__init__(self, mode, sensor_nums)
        self.sensor_nums = sensor_nums
        self.mode = mode

        self.pattern = {"train": 25, "test":10, "raw": 1000}
        #self.pattern = {"train": 250, "test":100, "raw": 1000, "other": 10}

    def fetch_numbers(self, matched_group):
        is_calibration = config.is_calibration
        console_input_number = config.console_input_number

        self.calibration_numbers = config.calibration_numbers

        make_serial_flush = False

        if self.pre_console_input_number != console_input_number:
            self.pre_console_input_number = console_input_number
            self.count = 0
            self.count2 = 0 #????
            fn = os.path.join(os.getcwd(), self.mode, console_input_number)
            if not os.path.exists(fn):
                if console_input_number != "1025":
                    os.makedirs(fn)
            else:
                nums_past_all_fn =  os.listdir(fn)
                nums_past_all = []
                for nums in nums_past_all_fn:
                    num, ext = os.path.splitext(os.path.splitext(nums)[0])
                    nums_past_all.append(int(num))
                if len(nums_past_all) != 0:
                    self.count = max(nums_past_all) + 1

        if matched_group == "a": #strat byte == a
            self.between_a_and_a = True
            self.result_list_nums = []
        elif self.between_a_and_a:
            self.result_list_nums.append(int(matched_group))

        if len(self.result_list_nums) == self.sensor_nums:
            self.between_a_and_a = False
            make_serial_flush = True
            if is_calibration:
                is_calibration = Calibrate.start_calibration(is_calibration, np.array(self.result_list_nums).astype(np.int64))

            if self.count < self.pattern[self.mode] and console_input_number.isdigit():
                if self.count2 < 5:
                    result_list = np.array(self.result_list_nums).astype(np.int64) - self.calibration_numbers
                    if console_input_number != "1025":
                        self.write_ceps(result_list, console_input_number)
                    print("Calibration Mode is ", is_calibration, ":input array = ", result_list, ":MODE = ", self.mode)

        return is_calibration, make_serial_flush
