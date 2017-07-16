import numpy as np
import DataSetup
import config
import Calibrate as cb

import reshape_array as ra

def setup():
    ver = config.ver

    train_x, train_y, test_x, test_y = DataSetup.read_ceps()

    fitted_data, num_labels = train(train_x, train_y)
    accuracy = test(fitted_data, test_x, test_y, num_labels)
    print(accuracy)

    return fitted_data

def train(train_x, train_y):
    sum_x = []
    count_y = []
    fitted_data = []
    for label, y in enumerate(train_y):
        if y == len(sum_x):
            sum_x.append(0)
            count_y.append(0)
        count_y[y] += 1
        #print(train_x, np.mean(train_x))
        sum_x[y] += train_x[label]
    for i in range(len(sum_x)):
        fitted_data.append(sum_x[i]/count_y[i])
    print(len(sum_x), len(fitted_data))
    return fitted_data, len(sum_x)

def test(fitted_data, test_x, test_y, num_labels):
    accuracy = 0
    for label, y in enumerate(test_y):
        distances = []
        for f_label, f in enumerate(fitted_data):
            distances.append(np.linalg.norm(f - test_x[label]))
        predict_label = np.argmin(distances)
        print("predict_label", predict_label, ":label", y)
        if predict_label == y:
            accuracy += 1

    return accuracy/len(test_x)

def stream(unused_addr, *raws):
    raw_list = np.array([float(r)*10.0 for r in raws]).astype(np.int64)
    config.is_calibration = cb.start_calibration(config.is_calibration, raw_list)
    xyz = raw_list - config.calibration_numbers
    #print(len(raws), xyz[0], len(xyz), len(config.calibration_numbers), len(config.fitted_data))
    #print(fitted_data, raw_list)

    dist = []
    aves = np.array([0 for n in range(132)]).astype(np.int64)

    for label, f in enumerate(config.fitted_data):
        dist.append(np.linalg.norm(f - xyz))
        #print(label, f - xyz)
    '''
    for f in fitted_data:
        count = 0
        for label, a in enumerate(raws):
            aves += a
            count += 1
        aves = aves/count
        dist.append(np.linalg.norm(f - aves))
    '''

    predict_label = np.argmin(dist)
    print("predict_label", predict_label, config.face_expression[predict_label])
