import numpy as np
from numpy.random import *

def make_new_reshaped_array(input_array, length_array):
    #x = np.arange(156).reshape(13, 12)
    x = input_array
    #print(x)
    x_shape = x.shape[0]
    #print(x.shape)
    want_choice_array = choice(np.arange(x.shape[0]), length_array, replace = False)
    sorted_list = sorted(want_choice_array)
    #print(sorted_list)
    #print(sorted_list)
    return x[sorted_list]
