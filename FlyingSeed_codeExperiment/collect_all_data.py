import os
import fnmatch
import shutil

path = '/media/hydroubuntu/Seagate Expansion Drive/data_lab_module_07122016/data_seed/'
destination = '/home/hydroubuntu/Desktop/Current/data_seed_experiment/'

# load list of all cases -------------------------------------------------------
list_cases = []
for file_name in os.listdir(path):
    if fnmatch.fnmatch(file_name, 'seed_*DIR'):
        list_cases.append(file_name)

print "Cases to process:"
for crrt_case in list_cases:
    print crrt_case

print " "
nbr_cases = len(list_cases)
print "Number of cases: " + str(nbr_cases)

# save all data to destination -------------------------------------------------
# list of all case names
with open(destination + 'list_all_cases.txt', 'w') as crrt_file:
    for crrt_case in list_cases:
        crrt_file.write(crrt_case)
        crrt_file.write('\n')

# calibration data
shutil.copy(path + 'poly_fit_calibration.npy', destination + 'poly_fit_calibration.npy')

# dict all results
shutil.copy(path + 'dict_all_results.pkl', destination + 'dict_all_results.pkl')

# data for each case
# analyse all cases ------------------------------------------------------------
for ind_case in range(nbr_cases):

    print ""
    print "------------------------------------------------------------"
    print "copy data for case: " + str(list_cases[ind_case])
    print "Case index: " + str(ind_case)

    # raw data generated from the images
    shutil.copy(path + list_cases[ind_case] + '/' + 'list_pos_seed.pkl', destination + list_cases[ind_case] + '_list_pos_seed.pkl')
    shutil.copy(path + list_cases[ind_case] + '/' + 'list_width_data_seed.pkl', destination + list_cases[ind_case] + '_list_width_data_seed.pkl')
    shutil.copy(path + list_cases[ind_case] + '/' + 'list_true_wing_tip.pkl', destination + list_cases[ind_case] + '_list_true_wing_tip.pkl')

    # valid range
    shutil.copy(path + list_cases[ind_case] + '/' + 'valid_range.csv', destination + list_cases[ind_case] + '_valid_range.csv')
