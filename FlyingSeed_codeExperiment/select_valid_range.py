from scipy import misc
import os
import fnmatch
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy import signal
from tqdm import tqdm
import pickle

# %matplotlib inline

#################################################################################
# all functions ----------------------------------------------------------------


class generateDataOnClick:
    def __init__(self, verbose=0):
        self.position_on_click_accumulator = []
        self.verbose = verbose

    def position_on_click(self, event):
        x, y = event.x, event.y
        if event.button == 1:
            if event.inaxes is not None:
                if self.verbose > 0:
                    print 'data coords:' + str(event.xdata) + " , " + str(event.ydata)
                self.position_on_click_accumulator.append((event.xdata, event.ydata))
                plt.axvline(event.xdata, color='r')
                plt.show()

    def return_positions(self):
        return self.position_on_click_accumulator


def select_valid_range(verbose=0):
    pos_seed = np.asarray(list_pos_seed)

    plt.figure()
    plt.plot(pos_seed[:, 0], label='x position')
    plt.plot(pos_seed[:, 1], label='y position')
    plt.xlabel('Frame number')
    plt.ylabel('Position seed (pxl)')
    plt.legend(loc=2)

    generate_data_on_click_object = generateDataOnClick()

    plt.connect('button_press_event', generate_data_on_click_object.position_on_click)
    plt.show()

    selected_positions_pixels = generate_data_on_click_object.return_positions()

    x_position_1 = int(np.floor(selected_positions_pixels[0][0]))
    x_position_2 = int(np.floor(selected_positions_pixels[1][0]))

    data_valid_range = np.array([x_position_1, x_position_2])

    # save the valid range
    np.savetxt(path + list_cases[ind_case] + '/' + "valid_range.csv", data_valid_range, delimiter=",")


def save_one_result(result_data, result_name):
    with open(path + list_cases[ind_case] + '/' + result_name + '.pkl', 'w') as crrt_file:
            pickle.dump(result_data, crrt_file, pickle.HIGHEST_PROTOCOL)


def load_one_result(result_name):
    with open(path + list_cases[ind_case] + '/' + result_name + '.pkl', 'r') as crrt_file:
            result_data = pickle.load(crrt_file)
    return result_data

#################################################################################

# analysis of the data
path = '/media/hydroubuntu/Seagate Expansion Drive/data_lab_module_07122016/data_seed/'
sampling_frequency = 30

# loads the calibration --------------------------------------------------------
poly_fit_calibration = np.load(path + 'poly_fit_calibration.npy')

# load list of all cases -------------------------------------------------------
list_cases = []
for file_name in os.listdir(path):
    if fnmatch.fnmatch(file_name, 'Test_*'):
        list_cases.append(file_name)

print "Cases to process:"
for crrt_case in list_cases:
    print crrt_case

print " "
nbr_cases = len(list_cases)
print "Number of cases: " + str(nbr_cases)

# select range on all cases ----------------------------------------------------
for ind_case in range(nbr_cases):

    print ""
    print "------------------------------------------------------------"
    print "Analysing case: " + str(list_cases[ind_case])

    path_to_images = path + list_cases[ind_case] + '/'

    print "Load generated data"

    list_pos_seed = load_one_result('list_pos_seed')
    list_width_data_seed = load_one_result('list_width_data_seed')
    list_true_wing_tip = load_one_result('list_true_wing_tip')

    print ""
    print "Select valid range"
    print "Click on the figure to select the range to use for later analysis"
    print "then close the figure."
    select_valid_range()
