import numpy as np
import config
import sys

def start_calibration(is_calibration, raws):
    input_array = raws
    if config.count_calibration < config.FRAMES_CALIBRATION:
        if is_calibration:
            config.count_calibration += 1
            config.array_calibration.append(input_array)
            print("Now calibrating", len(input_array))
    else:
        print("Calibration Finished", config.array_calibration)
        config.calibration_numbers = np.mean(np.array(config.array_calibration), axis=0)
        print(config.calibration_numbers)
        is_calibration = False
        config.count_calibration = 0
        config.array_calibration = []
    return is_calibration
