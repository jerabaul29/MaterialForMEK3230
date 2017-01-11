"""
Class for building some porous media in a similar fashion to

'3D printed porous media columns with fine control of column packing morphology'
    Journal of Chromatography A
"""

import numpy as np
import math
import sys
import random

sys.path.append('/usr/lib/freecad/lib/')
import FreeCAD

margin = 0.1


def check_distance_holes(center_x, center_y, radius, list_centers_x, list_centers_y, list_radiuses, verbose=False):
    """
    Check if the circle center_x, center_y, radius is outside of collision with the
    circles defined in the arrays.
    """

    length_arrays = len(list_centers_x)

    for ind in range(length_arrays):

        current_center_x = list_centers_x[ind]
        current_center_y = list_centers_y[ind]
        current_radius = list_radiuses[ind]

        if verbose:
            print "Data to compute distance to point " + str(ind)
            print "Center x"
            print center_x
            print current_center_x
            print "Center y"
            print center_y
            print current_center_y
            print "Radiuses"
            print radius
            print current_radius

        if (center_x - current_center_x)**2 + (center_y - current_center_y)**2 < (radius + current_radius + margin)**2:
            return False

    return True


def generate_random(min_value, max_value):
    """
    generate a random value from the uniform distribution in the interval
    [min, max)
    """

    return min_value + (max_value - min_value) * random.random()


class Porous_Medium():

    def __init__(self, perform_actions_current_document, verbose=False):

        self.perform_actions_current_document = perform_actions_current_document
        self.dummy_object = False

    def generate_one_slice_holes(self, dict_attributes, verbose=False):
        """
        Generate one slice

        Input: dict_attributes
            ['number_of_holes']
            ['radius_slice']
            ['min_size_holes']
            ['max_size_holes']

        Output: tuple data
            (list_centers_x, list_centers_y, list_radiuses)
        """

        number_of_holes = dict_attributes['number_of_holes']
        radius_slice = dict_attributes['radius_slice']
        min_size_holes = dict_attributes['min_size_holes']
        max_size_holes = dict_attributes['max_size_holes']

        list_centers_x = []
        list_centers_y = []
        list_radiuses = []

        number_of_valid_holes = 0
        total_area = 0

        while number_of_valid_holes < number_of_holes:

            if verbose:
                print "Generate hole: " + str(number_of_valid_holes)

            radius = generate_random(min_size_holes, max_size_holes)
            angle = generate_random(0, 2 * math.pi)
            radius_polar = generate_random(0, radius_slice - radius - margin)
            center_x = radius_polar * math.cos(angle)
            center_y = radius_polar * math.sin(angle)

            if check_distance_holes(center_x, center_y, radius, list_centers_x, list_centers_y, list_radiuses, verbose=verbose):

                list_centers_x.append(center_x)
                list_centers_y.append(center_y)
                list_radiuses.append(radius)

                number_of_valid_holes += 1
                total_area += np.pi * radius**2

        print "Total area of the holes: " + str(total_area)

        return (list_centers_x, list_centers_y, list_radiuses)

    def generate_data_slices_with_holes(self, dict_attributes, verbose=False):
        """
        Generate the positions for the slices

        Input: dict_attributes
            ['min_z']: minimum z position for slice
            ['max_z']: maximum z position for slice
            ['thickness_slices']: thickness of each solid slice
            ['spacing_slices']: spacing between the slices
            ['radius_slices']: radius of the slices
            ['number_of_holes']: number of holes in each slice
            ['min_size_holes']: min size of the holes
            ['max_size_holes']: max size of the holes

        Output: dict_slices
            ['number_of_slices']: the number of slices to use
            ['slice_i']: i the number of the slice. Each contains.
                 (pos_z, heigth, radius, list_centers_x, list_centers_y, list_radiuses)
        """

        min_z = dict_attributes['min_z']
        max_z = dict_attributes['max_z']
        thickness_slices = dict_attributes['thickness_slices']
        spacing_slices = dict_attributes['spacing_slices']
        radius_slices = dict_attributes['radius_slices']
        number_of_holes = dict_attributes['number_of_holes']
        min_size_holes = dict_attributes['min_size_holes']
        max_size_holes = dict_attributes['max_size_holes']

        # compute the number of slices to generate
        number_of_slices = int(math.floor((max_z - min_z) / (thickness_slices + spacing_slices)))

        if verbose:
            print "Using " + str(number_of_slices) + " slices"

        dict_slices = {}
        dict_slices['number_of_slices'] = number_of_slices

        dict_attributes_one_slice = {}
        dict_attributes_one_slice['number_of_holes'] = number_of_holes
        dict_attributes_one_slice['radius_slice'] = radius_slices
        dict_attributes_one_slice['min_size_holes'] = min_size_holes
        dict_attributes_one_slice['max_size_holes'] = max_size_holes

        for ind_slice in range(number_of_slices):

            if verbose:
                print "Generate slice " + str(ind_slice)

            pos_z = ind_slice * (thickness_slices + spacing_slices)

            data_one_slice = self.generate_one_slice_holes(dict_attributes_one_slice, verbose=verbose)

            dict_slices['slice_' + str(ind_slice)] = (pos_z, thickness_slices, radius_slices, data_one_slice[0],
                                                      data_one_slice[1], data_one_slice[2])

        return dict_slices

    def build_volume_nothing(self, verbose=False):
        """
        Build a dummy volume without anything in
        """

        self.dummy_object = True

    def add_slice(self, slice_data_tuple, slice_number, verbose=False):
        """
        Add one slice
        the slice_data_tuple is:
            (pos_z, heigth, radius, list_centers_x, list_centers_y, list_radiuses)
        """

        pos_z = slice_data_tuple[0]
        heigth = slice_data_tuple[1]
        radius = slice_data_tuple[2]
        list_centers_x = slice_data_tuple[3]
        list_centers_y = slice_data_tuple[4]
        list_radiuses = slice_data_tuple[5]

        # generate slice
        placement_medium = FreeCAD.Placement(
            FreeCAD.Vector(0, 0, pos_z),
            FreeCAD.Rotation(0, 0, 0),
            FreeCAD.Vector(0, 0, 0)
        )

        name_slice = 'full_slice_' + str(slice_number)

        self.perform_actions_current_document.add_cylinder(
            radius, heigth, placement_medium, name_slice, verbose=verbose
        )

        # make holes
        list_holes = []
        crrt_heigth = heigth + 2 * margin

        for ind in range(len(list_centers_x)):

            crrt_pos_x = list_centers_x[ind]
            crrt_pos_y = list_centers_y[ind]
            crrt_radius = list_radiuses[ind]

            placement_medium = FreeCAD.Placement(
                FreeCAD.Vector(crrt_pos_x, crrt_pos_y, pos_z - margin),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            name_hole = 'hole_' + str(ind) + '_slice_' + str(slice_number)

            self.perform_actions_current_document.add_cylinder(
                crrt_radius, crrt_heigth, placement_medium, name_hole, verbose=verbose
            )

            list_holes.append(name_hole)

        name_holes = 'holes_slice_' + str(slice_number)
        self.perform_actions_current_document.perform_union(list_holes, name_holes, verbose=verbose)

        name_final_slice = 'slice_with_holes_' + str(slice_number)
        self.perform_actions_current_document.perform_cut(name_slice, name_holes, name_final_slice, verbose=verbose)

    def generate_volume_slices(self, dict_slices, verbose=False):
        """
        Generate the volume corresponding to slices
        """

        number_of_slices = dict_slices['number_of_slices']

        list_name_final_slices = []

        for ind in range(number_of_slices):

            self.add_slice(dict_slices['slice_' + str(ind)], ind, verbose=verbose)
            name_final_slice = 'slice_with_holes_' + str(ind)
            list_name_final_slices.append(name_final_slice)

        self.perform_actions_current_document.perform_union(list_name_final_slices, 'porous_medium', verbose=verbose)

    def generate_box_around_medium(self, size_tuple, position_tuple, type_geometry_medium, wall_thickness=5, verbose=False):
        """
        Add the box around the porous medium
        """

        # a small quantity to make sure shapes touch to do union
        epsilon = margin

        if type_geometry_medium == 'circular':

            radius = size_tuple[0]
            size_z = size_tuple[1]

            pos_x = position_tuple[0]
            pos_y = position_tuple[1]
            pos_z = position_tuple[2]

            placement_medium = FreeCAD.Placement(
                FreeCAD.Vector(pos_x, pos_y, pos_z - wall_thickness),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            # generate the medium
            self.perform_actions_current_document.add_cylinder(
                radius + wall_thickness + margin, size_z + 2 * wall_thickness, placement_medium, 'wall_plain', verbose=verbose
            )

            self.perform_actions_current_document.add_cylinder(
                radius, size_z + 2 * wall_thickness, placement_medium, 'wall_empty', verbose=verbose
            )

            self.perform_actions_current_document.perform_cut('wall_plain', 'wall_empty', 'wall_lateral', verbose=verbose)

            self.perform_actions_current_document.add_cylinder(
                radius + wall_thickness * 10, size_z + 2 * wall_thickness, placement_medium, 'wall_plain_outside', verbose=verbose
            )

            self.perform_actions_current_document.add_cylinder(
                radius + wall_thickness, size_z + 2 * wall_thickness, placement_medium, 'wall_plain_2', verbose=verbose
            )

            self.perform_actions_current_document.perform_cut('wall_plain_outside', 'wall_plain_2', 'cut_outside_limit', verbose=verbose)

            list_shapes_union = [
                'wall_lateral',
                'porous_medium'
            ]

        else:
            raise("Porous medium geometry not implemented: " + str(type_geometry_medium))

        if not self.dummy_object:

            self.perform_actions_current_document.perform_union(list_shapes_union, 'porous_medium_with_walls_material_outside', verbose=verbose)

            self.perform_actions_current_document.perform_cut('porous_medium_with_walls_material_outside', 'cut_outside_limit', 'porous_medium_with_walls', verbose=verbose)

    def add_connectors_water(self, size_tuple, position_tuple, type_geometry_medium, dict_sizes, wall_thickness=5, verbose=False):
        """
        Add the connectors to the porous medium
        """

        if type_geometry_medium == 'circular':
            """
            the dictionary should then have the following fields:
                - height_cone
                - size_tube
                - radius_tube
                - wall_thickness
            """

            pos_x = position_tuple[0]
            pos_y = position_tuple[1]
            pos_z = position_tuple[2]

            radius = size_tuple[0]
            size_z = size_tuple[1]

            height_cone = dict_sizes["height_cone"]
            size_tube = dict_sizes["size_tube"]
            radius_tube = dict_sizes["radius_tube"]
            wall_thickness = dict_sizes["wall_thickness"]
            thickness_tube = dict_sizes["thickness_tube"]

            # connector in

            placement = FreeCAD.Placement(
                FreeCAD.Vector(pos_x, pos_y, pos_z - height_cone - margin),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            self.perform_actions_current_document.add_cone(radius_tube, radius, height_cone, placement, 'inside_cone_in', verbose=False)

            placement = FreeCAD.Placement(
                FreeCAD.Vector(pos_x, pos_y, pos_z - height_cone - margin),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            self.perform_actions_current_document.add_cone(radius_tube + wall_thickness, radius + wall_thickness, height_cone, placement, 'outside_cone_in', verbose=False)

            placement = FreeCAD.Placement(
                FreeCAD.Vector(pos_x, pos_y, pos_z - height_cone - size_tube + margin),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            self.perform_actions_current_document.add_cylinder(radius_tube, size_tube + 2 * margin, placement, 'inside_tube_in', verbose=False)

            placement = FreeCAD.Placement(
                FreeCAD.Vector(pos_x, pos_y, pos_z - height_cone - size_tube + margin),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            self.perform_actions_current_document.add_cylinder(radius_tube + thickness_tube, size_tube + 2 * margin, placement, 'outside_tube_in', verbose=False)

            self.perform_actions_current_document.perform_union(['inside_cone_in', 'inside_tube_in'], 'inside_in')
            self.perform_actions_current_document.perform_union(['outside_cone_in', 'outside_tube_in'], 'outside_in')
            self.perform_actions_current_document.perform_cut('outside_in', 'inside_in', 'connector_in')

            # connector out

            placement = FreeCAD.Placement(
                FreeCAD.Vector(pos_x, pos_y, pos_z + size_z + margin),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            self.perform_actions_current_document.add_cone(radius, radius_tube, height_cone, placement, 'inside_cone_out', verbose=False)

            placement = FreeCAD.Placement(
                FreeCAD.Vector(pos_x, pos_y, pos_z + size_z + margin),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            self.perform_actions_current_document.add_cone(radius + wall_thickness, radius_tube + wall_thickness, height_cone, placement, 'outside_cone_out', verbose=False)

            placement = FreeCAD.Placement(
                FreeCAD.Vector(pos_x, pos_y, pos_z + size_z + height_cone - margin),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            self.perform_actions_current_document.add_cylinder(radius_tube, size_tube + 2 * margin, placement, 'inside_tube_out', verbose=False)

            placement = FreeCAD.Placement(
                FreeCAD.Vector(pos_x, pos_y, pos_z + size_z + height_cone - margin),
                FreeCAD.Rotation(0, 0, 0),
                FreeCAD.Vector(0, 0, 0)
            )

            self.perform_actions_current_document.add_cylinder(radius_tube + thickness_tube, size_tube + 2 * margin, placement, 'outside_tube_out', verbose=False)

            self.perform_actions_current_document.perform_union(['inside_cone_out', 'inside_tube_out'], 'inside_out')
            self.perform_actions_current_document.perform_union(['outside_cone_out', 'outside_tube_out'], 'outside_out')
            self.perform_actions_current_document.perform_cut('outside_out', 'inside_out', 'connector_out')

            if not self.dummy_object:

                # put all together
                self.perform_actions_current_document.perform_union(['porous_medium_with_walls', 'connector_in', 'connector_out'], 'porous_medium_with_walls_connectors')

            else:

                # put all together
                self.perform_actions_current_document.perform_union(['wall_lateral', 'connector_in', 'connector_out'], 'empty_medium_with_walls_connectors')

        else:
            raise("Porous medium geometry not implemented: " + str(type_geometry_medium))

    def add_pressure_taps(self, dict_attributes, verbose=False):
        """
        Add the pressure taps to the porous medium with connector walls

        the dict_attributes should have the following fields:
            - length_connectors
            - radius_hole_connectors
            - wall_thickness_connectors
            - pos_z_1
            - pos_z_2
            - pos_y
        """

        # CODE TO REMOVE BEFORE GIVING TO THE STUDENTS -------------------------
        pass
