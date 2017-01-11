import numpy as np
import pickle


def coefficient_Poiseuille_flow(radius, L, mu):
    """ compute the coefficient of proportionality between mass flow rate and
    pressure drop for a Poiseuille flow
    """
    # CODE TO REMOVE BEFORE GIVING TO THE STUDENTS -------------------------
    pass


def coefficient_one_slice(slice_data, mu, verbose=False):
    """ compute the coefficient of proportionaliry between mass flow rate and
    pressure drop along one slice with each channel following Poiseuille flow
    """

    # CODE TO REMOVE BEFORE GIVING TO THE STUDENTS -------------------------
    pass


def coefficient_all_slices(slice_dict, mu, verbose=False):
    """ compute the coefficient of proportionality between pressure drop and mass
    flow rate over all the slices
    """

    # CODE TO REMOVE BEFORE GIVING TO THE STUDENTS -------------------------
    pass

# name of the document
freecad_doc_name = 'test_porous_media_packing_morphology' + str(attempt)
# path on which the document should be
freecad_doc_path = '/home/hydroubuntu/Desktop/Current/'

with open(freecad_doc_path + freecad_doc_name + '.pkl', 'r') as current_file:
        dict_slices_data = pickle.load(current_file)

mu_water = 1.0e-3
coefficient_darcy = coefficient_all_slices(dict_slices_data, mu_water)

print "Theoretical coefficient in the Darcy law: Delta_P = " + str(coefficient_darcy) + ' Q'
print "                                          Q = " + str(1. / coefficient_darcy) + " Delta_P"
