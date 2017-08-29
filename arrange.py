import numpy as np
from scipy import signal
from pylab import *
import os

import shutil

import config
import Calibrate

class Arrange:
    pre_console_input_number = "xx"
    between_a_and_a = False

    count = 0
    count2 = 0 #こいつなんで存在しているのかわかっていない

    result_list_nums = []

    count_calibration = config.count_calibration
    FRAMES_CALIBRATION = config.FRAMES_CALIBRATION
    array_calibration = config.array_calibration


    mouth_gestures = []

    def __init__(self, mode, sensor_nums):
        self.mode = mode
        self.sensor_nums = sensor_nums
        self.calibration_numbers = np.array([0 for n in range(sensor_nums)]).astype(np.int64)
        config.calibration_numbers = self.calibration_numbers

    def make_dir_train_or_test(self, is_new):
        if self.mode == "test" or self.mode == "train":
            fn = os.path.join(os.getcwd(), self.mode)
            if not os.path.exists(fn):
                os.makedirs(fn)
            elif is_new == "n":
                nums = []
                list_dirs = os.listdir(os.getcwd())
                for d in list_dirs:
                    if d[0:len(self.mode)] == self.mode:
                        exist_str = d[len(self.mode) + 1:]
                        if exist_str == "":
                            nums.append(0)
                        else:
                            nums.append(int(exist_str))
                if nums == []:
                    maxnum = 0
                else:
                    maxnum = np.max(nums)

                if maxnum < 9:
                    str_num = "0" + str(maxnum + 1)
                else:
                    str_num = str(maxnum + 1)
                os.rename(os.path.join(os.getcwd(), self.mode), os.path.join(os.getcwd(), self.mode + str_num))
                os.makedirs(os.path.join(os.getcwd(), self.mode))
            else:
                fn = os.path.join(os.getcwd(), config.username)
                if not os.path.exists(fn):
                    os.makedirs(fn)

    def write_ceps(self, ceps, filename):
        if True:
            if self.mode == "test" or self.mode == "train":
                filename_mode = self.mode
            else:
                filename_mode = config.username
            fn = os.path.join(os.getcwd(), filename_mode, filename)
            if not os.path.exists(fn):
                os.makedirs(fn)
            #base_fn,ext = os.path.splitext(fn)
            count_str = "00"
            if self.count < 10:
                count_str = "0" + str(self.count)
            else:
                count_str = str(self.count)
            data_fn = os.path.join(filename_mode, filename, count_str + ".ceps")
            np.save(data_fn, ceps)
            self.count += 1
            self.count2 += 1
