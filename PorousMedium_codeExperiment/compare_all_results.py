"""
import all results in different configurations and analyse them together
"""

import numpy as np
import os
import fnmatch
import matplotlib.pyplot as plt

path = 'data/'

# load all results -------------------------------------------------------------
list_all_results_files = []

for crrt_file in os.listdir(path):
    if fnmatch.fnmatch(crrt_file, '*_results.csv'):
            list_all_results_files.append(crrt_file)

print "Found results files:"
print list_all_results_files

dict_all_results = {}
for crrt_file in list_all_results_files:
    dict_all_results[crrt_file] = np.genfromtxt(path + crrt_file, delimiter=',')

# plot all results together ----------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(111)

for crrt_file in list_all_results_files:
    crrt_result = dict_all_results[crrt_file]
    crrt_sorted_mean_pressures = crrt_result[:, 0]
    crrt_sorted_mass_flow_rates = crrt_result[:, 1]

    plt.plot(crrt_sorted_mean_pressures, crrt_sorted_mass_flow_rates, label=crrt_file, marker='o')

plt.xlabel('Mean pressure drop (kPa)')
plt.ylabel('Mass flow rate (g / s)')
# plt.legend(bbox_to_anchor=(-0.1, 1.25), loc='upper left', ncol=1)
lgd = ax.legend(bbox_to_anchor=(-0.1, 1.25), loc='upper left', ncol=1)
plt.show()

fig.savefig('comparison_all_results', bbox_extra_artists=(lgd,), bbox_inches='tight')
