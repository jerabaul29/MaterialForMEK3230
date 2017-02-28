"""
This code can be used to log simultaneously the pressure sensor and scale.

Adjust the parameters in the PARAMETERS FOR THE LOGGING.

In particular, you will have to change the name_case.
               you may want to adjust the time_logging.
"""

import serial
import numpy as np
import matplotlib.pyplot as plt
import time
import glob
from StringIO import StringIO
import matplotlib.pyplot as plt

################################################################################
# START PARAMETERS FOR THE LOGGING
################################################################################
# parameters that determine how the logging is performed

# debugging: print additional output
debug = False

# usb ports for pressure sensor and scale
# for detection of usb inputs, use: $ ls /dev/ttyACM*
usb_port_name_pressure = '/dev/ttyACM1'
usb_port_name_scale = '/dev/ttyACM2'

# frequency of pressure logging is determined by the script running on the
# Arduino board. See the Arduino board sketch for changing this parameter.

# frequency of weight logging in Hz
frequency_logging_weight = 10

# logging time in s
time_logging = 30

# where to save the results
path = 'data/'
name_case = '3Dprint_1_case_water_run_1'

################################################################################
# END PARAMETERS FOR THE LOGGING
################################################################################

# functions for control of the usb port and convert data -----------------------


def look_for_available_ports():
    '''find available serial ports to Arduino
    '''
    available_ports = glob.glob('/dev/ttyACM*')
    return available_ports


def connect_to_board(usb_port_name=None, baud_rate=9600):
    """connect to the board on USB
    """

    if usb_port_name is None:
        # find available port
        port = look_for_available_ports()

        # if none stop here
        if not port:
            print "No board available"
            return

        # if some, take the first
        print "Using port: " + str(port[0])
        usb_port_name = str(port[0])

    usb_port = serial.Serial(usb_port_name, baudrate=baud_rate, timeout=0.5)
    usb_port.flushInput()

    print "Port imported: " + usb_port_name

    # return the port for external use if needed
    return(usb_port)


def convert_list_feedback(list_feedback):
    """convert a list feedback into a numpy array"""

    # remove the first item: comma
    list_feedback.pop(0)

    # generate the string
    string_feedback = StringIO(''.join(list_feedback))

    # generate as numpy table
    numpy_feedback = np.genfromtxt(string_feedback, delimiter=",")

    return numpy_feedback


available_ports = look_for_available_ports()

print "Available ports: " + str(available_ports)
print "Note that the first ttyACM may be used for the computer serial adapter"

# prepare the logging of the pressure ------------------------------------------
pressure_data = []
pressure_time = []

usb_port_pressure = connect_to_board(usb_port_name=usb_port_name_pressure, baud_rate=57600)

# prepare the logging of the weight --------------------------------------------
weight_data = []
weight_time = []

delay_logging_pressure = 1.0 / frequency_logging_weight

usb_port_weight = connect_to_board(usb_port_name=usb_port_name_scale, baud_rate=9600)

# do the logging ---------------------------------------------------------------

wait_for_data = raw_input("Press enter to start logging for " + str(time_logging) + ' seconds')

time_init = time.time()
last_logging_pressure = time_init

while (time.time() - time_init < time_logging):

    # take care of the pressure ################################################
    if usb_port_pressure.inWaiting > 0:
        char_read = usb_port_pressure.read()

        if debug:
            print "Received: " + str(char_read)

        # if a new measurement, post the last one, write time received, start
        # a new log
        if char_read == 'A':
            pressure_time.append(time.time() - time_init)
            pressure_data.append(',')

        else:
            pressure_data.append(char_read)

    # take care of the weight ##################################################
    # if it is time to do a weight measurement, ask for a value
    if (time.time() - last_logging_pressure > delay_logging_pressure):
        last_logging_pressure += delay_logging_pressure
        weight_time.append(time.time() - time_init)

        usb_port_weight.write('SI\n')

        end_of_answer = False

        while not end_of_answer:
            if usb_port_weight.inWaiting > 0:
                char_read = usb_port_weight.read()

                if debug:
                    print "Received: " + str(char_read)

                if char_read == ' ':
                    pass

                elif char_read == '\r':
                    pass

                elif char_read.isalpha():
                    pass

                elif char_read == '\n':
                    end_of_answer = True

                else:
                    weight_data.append(char_read)

        weight_data.append(',')

if debug:
    print "Logged pressure_data: "
    print pressure_data
    print "Logged pressure_time: "
    print pressure_time

    print "Logged weight_data: "
    print weight_data
    print "logged weight_time: "
    print weight_time

# convert the logged data ------------------------------------------------------
pressure_data_array_raw = convert_list_feedback(pressure_data)
min_length_pressure = min(pressure_data_array_raw.shape[0], len(pressure_time))

pressure_data_array = pressure_data_array_raw[1: min_length_pressure - 1]
pressure_time = pressure_time[1: min_length_pressure - 1]

weight_data_array_raw = convert_list_feedback(weight_data)
min_length_weight = min(weight_data_array_raw.shape[0], len(weight_time))

weight_data_array = weight_data_array_raw[1: min_length_weight - 1]
weight_time = weight_time[1: min_length_weight - 1]

# plot the data ----------------------------------------------------------------
plt.figure()
plt.plot(pressure_time, pressure_data_array, label='pressure raw data')
plt.legend()
plt.show()

plt.figure()
plt.plot(weight_time, weight_data_array, label='weight raw data')
plt.legend()
plt.show()

# save the data ----------------------------------------------------------------

# save as csv
np.savetxt(path + name_case + "_tp.csv", pressure_time, delimiter=",")
np.savetxt(path + name_case + "_dp.csv", pressure_data_array, delimiter=",")
np.savetxt(path + name_case + "_tw.csv", weight_time, delimiter=",")
np.savetxt(path + name_case + "_dw.csv", weight_data_array, delimiter=",")
