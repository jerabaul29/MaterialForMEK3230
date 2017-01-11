import porous_medium
import perform_actions_document
import import_freecad
import numpy as np
import pickle

# import freecad ---------------------------------------------------------------
import_freecad.import_fcstd(import_freecad.FREECADPATH)

verbose = False


# paths etc --------------------------------------------------------------------
# name of the document to generate in FreeCAD
freecad_doc_name = 'porous_media_slices_1'
# path on which the document should be saved
freecad_doc_path = '/home/hydroubuntu/Desktop/Current/'
# extension to use when saving freecad files
freecad_extension = '.fcstd'

# create class instances -------------------------------------------------------
# create a new document
working_doc = FreeCAD.newDocument(freecad_doc_name)
# create a perform action class on this document
action_class = perform_actions_document.Perform_Actions_Document(working_doc, verbose=verbose)
# create a porous medium class on the action class
porous_media_instance = porous_medium.Porous_Medium(action_class, verbose=verbose)


# parameters for building the geometry -----------------------------------------
# general properites of the medium and box
length = 40.
radius = 12.5
pos_x = 0.
pos_y = 0.
pos_z = 0.
geometry_medium = 'circular'
wall_thickness = 8

# dict attributes for building slices
dict_attributes = {}
dict_attributes['min_z'] = 0
dict_attributes['max_z'] = length
dict_attributes['thickness_slices'] = 4
dict_attributes['spacing_slices'] = 3
dict_attributes['radius_slices'] = radius
dict_attributes['number_of_holes'] = 10
dict_attributes['min_size_holes'] = 0.3
dict_attributes['max_size_holes'] = 0.5

# properties and dict for building connectors
radius_connectors = 5.
radius_tube = 1.5
# dict for connectors
dict_sizes_connectors = {
    "height_cone": 25,
    "size_tube": 15,
    # "radius_tube": 3,
    "radius_tube": radius_tube,
    "wall_thickness": wall_thickness,
    # "thickness_tube": 2.1
    "thickness_tube": radius_connectors - radius_tube
}

# properties and dict for building the pressure taps
radius_pressure_taps = 3.0
hole_pressure_taps = 0.75
# dict for pressure taps
dict_attributes_pressure_taps = {
    "length_connectors": 20,
    "radius_hole_connectors": hole_pressure_taps,
    "wall_thickness_connectors": radius_pressure_taps - hole_pressure_taps,
    "pos_z_1": -15,
    "pos_z_2": 55,
    "pos_y": -10,  # NOTE: must be negative!!
}


# generate the medium ----------------------------------------------------------
print "Generate data for holes"
dict_slices_data = porous_media_instance.generate_data_slices_with_holes(dict_attributes, verbose=verbose)

print "Generate porous medium"
porous_media_instance.generate_volume_slices(dict_slices_data, verbose=verbose)

# properties for box generation
size_tuple = (radius, length)
position_tuple = (pos_x, pos_y, pos_z)
type_geometry_medium = geometry_medium

print "Generate box"
porous_media_instance.generate_box_around_medium(size_tuple, position_tuple, type_geometry_medium, wall_thickness=wall_thickness, verbose=verbose)

print "Total area of the inlet /outlet: " + str(np.pi * dict_sizes_connectors["radius_tube"]**2)

print "Generate connectors"
porous_media_instance.add_connectors_water(size_tuple, position_tuple, type_geometry_medium, dict_sizes_connectors, wall_thickness=wall_thickness, verbose=verbose)

print "Add pressure measurement connectors"
# note: I took away the body of this function in the Porous_Medium class, so you will have to write it by yourself.
porous_media_instance.add_pressure_taps(dict_attributes_pressure_taps, verbose=verbose)


# save -------------------------------------------------------------------------
print "Save CAD model"
working_doc.saveAs(freecad_doc_path + freecad_doc_name + freecad_extension)

print "Save slice informations"
with open(freecad_doc_path + freecad_doc_name + '.pkl', 'w') as crrt_file:
        pickle.dump(dict_slices_data, crrt_file, pickle.HIGHEST_PROTOCOL)
