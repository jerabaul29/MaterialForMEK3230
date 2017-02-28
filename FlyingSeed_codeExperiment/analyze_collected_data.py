import fnmatch
import pickle
from parse import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

%matplotlib inline

path_to_data = '/home/hydroubuntu/Desktop/Current/data_seed_experiment_07122016/'
path_save_figures = '/home/hydroubuntu/Desktop/Current/figures_seed_experiment_07122016/'

# load the list of case names --------------------------------------------------
list_cases = []
with open(path_to_data + 'list_all_cases.txt', 'r') as crrt_file:
    for crrt_line in crrt_file:
        list_cases.append(crrt_line[:-1])

nbr_cases = len(list_cases)

print " "
print "-------------------------------"
print "Number of cases (list_all_cases.txt): " + str(nbr_cases)
print "Loaded cases:"
for crrt_case in list_cases:
    print crrt_case

# load the results directory ---------------------------------------------------
print ""
print "Load results directory"

with open(path_to_data + 'dict_all_results.pkl', 'r') as crrt_file:
        dict_all_results = pickle.load(crrt_file)

# parse the file names ---------------------------------------------------------
dict_properties_case = {}
list_wing_types = []
list_weight_load = []
list_repetition = []

for crrt_case in list_cases:

    wing_type = parse("seed_{}_{}", crrt_case)[0]
    if wing_type == 'thicker':
        wing_type = 'thickest'
    dict_properties_case[crrt_case + "_wing_type"] = wing_type
    list_wing_types.append(wing_type)

    weight_load = parse("seed_{}_{}lead{}", crrt_case)[1]
    dict_properties_case[crrt_case + "_weight_load"] = int(weight_load)
    list_weight_load.append(weight_load)

    repetition = parse("{}_repetition{}.mkvDIR", crrt_case)
    if repetition is not None:
        dict_properties_case[crrt_case + "_repetition"] = repetition[1]
    else:
        dict_properties_case[crrt_case + "_repetition"] = '0'
    list_repetition.append(dict_properties_case[crrt_case + "_repetition"])

# put all the data in one pandas -----------------------------------------------
df = pd.DataFrame(list_cases)
df['wing_type'] = list_wing_types
df['weight_load'] = list_weight_load
df['repetition'] = list_repetition

list_mean_vertical_velocity = []
list_averaged_seed_rotation = []

for crrt_case in list_cases:
    list_mean_vertical_velocity.append(dict_all_results[crrt_case + "mean_vertical_velocity"])
    list_averaged_seed_rotation.append(dict_all_results[crrt_case + "averaged_seed_rotation"])

df['averaged_seed_rotation'] = list_averaged_seed_rotation
df['mean_vertical_velocity'] = list_mean_vertical_velocity

# compute some data on pandas columns ------------------------------------------
df['pitch_angle'] = np.abs(df['averaged_seed_rotation'] / df['mean_vertical_velocity'])

# just a few examples of how to use pands --------------------------------------

# data frame
df

# how to extract all cases with wing_type being intermediate
df[df['wing_type'] == 'intermediate']

# do some plotting -------------------------------------------------------------

# PUT YOUR CODE HERE!
