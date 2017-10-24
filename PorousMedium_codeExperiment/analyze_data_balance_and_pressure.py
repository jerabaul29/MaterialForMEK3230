"""
Some code to help you analyse the data from the porous medium experiment.

Adjust the parameters in the PARAMETERS FOR THE LOGGING.

Fill in the body of the function convert_pressure with the calibration data
for the sensor.

If you need to do more than what is here, remember that all the data generated
is saved as a csv by the last line of the script.
"""

import numpy as np
import matplotlib.pyplot as plt

################################################################################
# START PARAMETERS FOR THE LOGGING
################################################################################

debug = False

# path to the data, format of the data file names and number of cases in the
# corresponding case
path = '/mn/sarpanitu/ansatte-u3/jeanra/Desktop/Current/gruppe_3/'
base_name = '3Dprint_group_3_run_'
number_of_cases = 6

# select by hand the valid range on the data, to use for analysis
# you will need to do this at least the first time you study a new set of
# measurements; then, you can just use again the ranges you generated.
perform_range_selection = True

# show all measurements loaded, indicating the valid range chosen
show_images_all = True

g = 9.81

################################################################################
# END PARAMETERS FOR THE LOGGING
################################################################################


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


def convert_pressure(raw_pressure_array):
    """Convert pressure from raw to kPa

    According to data sheet:
    V_out = 5.0 * (0.09*P + 0.04)

    remember that the Arduino is an ADC, so that:
    V_out = 5.0 / 1023.0 * raw_pressure_array

    Use your own calibration to fill in the body of the function.
    """


    # body of the ufnction to complete by the students
    V_out = 5.0 / 1023.0 * raw_pressure_array
    pressure_kpa = (V_out / 5.0 - 0.04) / 0.09

    return pressure_kpa

# load all data ----------------------------------------------------------------
file_suffix_list = ['_tp', '_dp', '_tw', '_dw']

dict_data = {}

for current_test_number in range(number_of_cases):
    current_name_case = path + base_name + str(current_test_number + 1)

    for current_suffix in file_suffix_list:
        current_name_file = current_name_case + current_suffix + '.csv'
        dict_data[current_name_file] = np.genfromtxt(current_name_file, delimiter=',')

# select the useful time for each data set  ------------------------------------

if perform_range_selection:

    print "For each case, select the range of interest by clicking on the figure, then close the figure"

    for current_file_number in range(number_of_cases):
        not_satisfied = True

        while not_satisfied:
            plt.figure()
            plt.plot(dict_data[path + base_name + str(current_file_number + 1) + '_dp.csv'])
            plt.xlabel('measurement number')
            plt.ylabel('raw pressure')

            generate_data_on_click_object = generateDataOnClick()

            plt.connect('button_press_event', generate_data_on_click_object.position_on_click)
            plt.show()

            selected_positions_pixels = generate_data_on_click_object.return_positions()

            satisfied = raw_input("Satisfied? [y]: ")
            satisfied = 'y'

            if satisfied == 'y':
                not_satisfied = False

                accumulator = generate_data_on_click_object.return_positions()
                x_position_1 = int(np.floor(accumulator[0][0]))
                x_position_2 = int(np.floor(accumulator[1][0]))

                data_valid_range = np.array([x_position_1, x_position_2])

                # save the valid range for pressure
                np.savetxt(path + base_name + str(current_file_number + 1) + "_vrp.csv", data_valid_range, delimiter=",")

                # compute valid range for weight
                min_ind_w = np.where(dict_data[path + base_name + str(current_file_number + 1) + '_tw.csv'] > dict_data[path + base_name + str(current_file_number + 1) + '_tp.csv'][x_position_1])[0]
                max_ind_w = np.where(dict_data[path + base_name + str(current_file_number + 1) + '_tw.csv'] > dict_data[path + base_name + str(current_file_number + 1) + '_tp.csv'][x_position_2])[0]

                data_valid_range = np.array([min_ind_w[0], max_ind_w[0]])

                # save the valid range for weight
                np.savetxt(path + base_name + str(current_file_number + 1) + "_vrw.csv", data_valid_range, delimiter=",")


# load the valid range data ----------------------------------------------------
for current_file_number in range(number_of_cases):
    current_name_range_valid_vrp = path + base_name + str(current_file_number + 1) + "_vrp.csv"
    dict_data[current_name_range_valid_vrp] = np.genfromtxt(current_name_range_valid_vrp, delimiter=',')

    current_name_range_valid_vrw = path + base_name + str(current_file_number + 1) + "_vrw.csv"
    dict_data[current_name_range_valid_vrw] = np.genfromtxt(current_name_range_valid_vrw, delimiter=',')

    if show_images_all:
        # show pressure
        plt.figure()
        plt.plot(
            dict_data[path + base_name + str(current_file_number + 1) + '_tp.csv'],
            dict_data[path + base_name + str(current_file_number + 1) + '_dp.csv'],
            color='b'
        )
        plt.axvline(dict_data[path + base_name + str(current_file_number + 1) + '_tp.csv'][int(dict_data[current_name_range_valid_vrp][0])], color='g')
        plt.axvline(dict_data[path + base_name + str(current_file_number + 1) + '_tp.csv'][int(dict_data[current_name_range_valid_vrp][1])], color='r')

        plt.xlabel('Time (s)')
        plt.ylabel('Raw pressure')
        plt.title('Case ' + str(current_file_number))

        plt.show()

        # show weight
        plt.figure()
        plt.plot(
            dict_data[path + base_name + str(current_file_number + 1) + '_tw.csv'],
            dict_data[path + base_name + str(current_file_number + 1) + '_dw.csv'],
            color='b'
        )
        plt.axvline(dict_data[path + base_name + str(current_file_number + 1) + '_tw.csv'][int(dict_data[current_name_range_valid_vrw][0])], color='g')
        plt.axvline(dict_data[path + base_name + str(current_file_number + 1) + '_tw.csv'][int(dict_data[current_name_range_valid_vrw][1])], color='r')

        plt.xlabel('Time (s)')
        plt.ylabel('Mass')
        plt.title('Case ' + str(current_file_number))

        plt.show()

# perform analysis -------------------------------------------------------------
list_mean_pressures = []
list_mass_flow_rates = []

for current_file_number in range(number_of_cases):
    current_name_case = path + base_name + str(current_file_number + 1)

    print "look at current name: " + str(current_name_case)

    # analysis of the pressure data ############################################
    # compute the mean pressure
    pressure_data = convert_pressure(dict_data[current_name_case + '_dp.csv'])
    pressure_vr = dict_data[current_name_case + '_vrp.csv']

    mean_valid_pressure = np.mean(pressure_data[pressure_vr[0]: pressure_vr[1]])

    print "mean_valid_pressure: " + str(mean_valid_pressure)

    list_mean_pressures.append(mean_valid_pressure)

    # analysis of the mass data ################################################
    weight_data = dict_data[current_name_case + '_dw.csv']
    weight_time = dict_data[current_name_case + '_tw.csv']
    weight_vr = dict_data[current_name_case + '_vrw.csv']

    mass_increase = (weight_data[weight_vr[1]] - weight_data[weight_vr[0]])
    time_mass_increase = weight_time[weight_vr[1]] - weight_time[weight_vr[0]]

    mean_mass_flow_rate = mass_increase / time_mass_increase

    print "mean_mass_flow_rate: " + str(mean_mass_flow_rate)

    list_mass_flow_rates.append(mean_mass_flow_rate)

# translate to numpy and order the data
mean_pressures = np.array(list_mean_pressures)
mass_flow_rates = np.array(list_mass_flow_rates)

ordered_indexes = np.argsort(mean_pressures)

sorted_mean_pressures = mean_pressures[ordered_indexes]
sorted_mass_flow_rates = mass_flow_rates[ordered_indexes]

# plot result
plt.figure()
plt.plot(sorted_mean_pressures, sorted_mass_flow_rates, marker='o', color='b')
plt.xlabel('mean pressure drop (kPa)')
plt.ylabel('mass flow rate (g / s)')
plt.xlim([0, 10])
plt.ylim([0, 0.28])
plt.show()

# save the results for later use
results = np.zeros((number_of_cases, 2))
results[:, 0] = sorted_mean_pressures
results[:, 1] = sorted_mass_flow_rates

np.savetxt(path + base_name + "_results.csv", results, delimiter=",")
