import fnmatch
import pickle
from parse import *
import numpy as np
import matplotlib.pyplot as plt

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

# you will have to write your own code!
# note that, if you used correct path names, all the data generated is in: dict_all_results
# you can look at what data is in dict_all_results using:

for crrt_key in dict_all_results.keys():
    print("crrt_key: " + crrt_key)
    
# you want to use the data corresponding to the seed mean vertical velocity and
# rotation frequency
