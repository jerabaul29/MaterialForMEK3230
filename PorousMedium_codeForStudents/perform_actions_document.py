"""
A class for performing actions on a FreeCAD document
"""

from import_freecad import *

import_fcstd(FREECADPATH)

import OpenSCADUtils
import Mesh
import BuildRegularGeoms


class Perform_Actions_Document():

    def __init__(self, document, verbose=False):
        """
        Define which document to work on
        """

        if verbose:
            print "Init perform_actions_document class"

        self.document = document

    def recompute(self):
        """
        recompute underlying FreeCAD document
        """

        self.document.recompute()

    def add_sphere(self, radius, placement, name, verbose=False):
        """
        Add a sphere to the document
        """

        if verbose:
            print "Add a sphere"

        self.document.addObject('Part::Sphere', name)

        self.document.getObject(name).Radius = radius
        self.document.getObject(name).Placement = placement

        self.document.recompute()

    def add_sphere_mesh(self, radius, placement, name, sampling=50, verbose=False):
        """
        Add a sphere to the document
        """

        if verbose:
            print "Add a sphere"

        self.document.addObject('Mesh::Sphere', name)

        self.document.getObject(name).Radius = radius
        self.document.getObject(name).Placement = placement
        self.document.getObject(name).Sampling = sampling

        self.document.recompute()

    def add_cylinder(self, radius, height, placement, name, verbose=False):
        """
        Add a cylinder to the document
        """

        if verbose:
            print "Add a cylinder"

        self.document.addObject('Part::Cylinder', name)

        self.document.getObject(name).Radius = radius
        self.document.getObject(name).Height = height
        self.document.getObject(name).Placement = placement

        self.document.recompute()

    def add_cylinder_mesh(self, radius, height, placement, name, edge_length=1, sampling=50, verbose=False):
        """
        Add a cylinder to the document
        """

        if verbose:
            print "Add a cylinder"

        self.document.addObject('Mesh::Cylinder', name)

        self.document.getObject(name).Radius = radius
        self.document.getObject(name).Length = height
        self.document.getObject(name).Placement = placement
        self.document.getObject(name).EdgeLength = edge_length
        self.document.getObject(name).Sampling = sampling

        self.document.recompute()

    def add_rectangle(self, size_x, size_y, size_z, placement, name, verbose=False):
        """
        Add a rectangle
        """

        if verbose:
            print "Add a rectangle"

        self.document.addObject('Part::Box', name)

        self.document.getObject(name).Length = size_x
        self.document.getObject(name).Width = size_y
        self.document.getObject(name).Height = size_z
        self.document.getObject(name).Placement = placement

        self.document.recompute()

    def add_rectangle_mesh(self, size_x, size_y, size_z, placement, name, verbose=False):
        """
        Add a rectangle
        """

        if verbose:
            print "Add a rectangle"

        self.document.addObject('Mesh::Cube', name)

        self.document.getObject(name).Length = size_x
        self.document.getObject(name).Width = size_y
        self.document.getObject(name).Height = size_z
        self.document.getObject(name).Placement = placement

        self.document.recompute()

    def add_cone(self, radius_1, radius_2, size_z, placement, name, verbose=False):
        """
        Add a conne
        """

        if verbose:
            print "Add a cone"

        self.document.addObject('Part::Cone', name)

        self.document.getObject(name).Radius1 = radius_1
        self.document.getObject(name).Radius2 = radius_2
        self.document.getObject(name).Height = size_z
        self.document.getObject(name).Placement = placement

        self.document.recompute()

    def add_cone_mesh(self, radius_1, radius_2, size_z, placement, name, edge_length=1, sampling=50, verbose=False):
        """
        Add a conne
        """

        if verbose:
            print "Add a cone"

        self.document.addObject('Mesh::Cone', name)

        self.document.getObject(name).Radius1 = radius_1
        self.document.getObject(name).Radius2 = radius_2
        self.document.getObject(name).Length = size_z
        self.document.getObject(name).Placement = placement
        self.document.getObject(name).EdgeLength = edge_length
        self.document.getObject(name).Sampling = sampling

        self.document.recompute()

    def add_wedge(self, x_min, x_max, y_min, y_max, z_min, z_max, x2_min, x2_max, z2_min, z2_max, placement, name, verbose=False):
        """
        Add a wedge
        """

        if verbose:
            print "Add a cone"

        self.document.addObject('Part::Wedge', name)

        self.document.getObject(name).Xmax = x_max
        self.document.getObject(name).Xmin = x_min
        self.document.getObject(name).Ymin = y_min
        self.document.getObject(name).Ymax = y_max
        self.document.getObject(name).Zmin = z_min
        self.document.getObject(name).Zmax = z_max
        self.document.getObject(name).X2min = x2_min
        self.document.getObject(name).X2max = x2_max
        self.document.getObject(name).Z2min = z2_min
        self.document.getObject(name).Z2max = z2_max
        self.document.getObject(name).Placement = placement

        self.document.recompute()

    def perform_union(self, list_objects_names, name, verbose=False):
        """
        Perform the union of all shapes given in list_objects_names.
        The final shape is called name. Intermediate shapes are called shape_n,
        where n is an indice that indicates how many fusions left to do
        """

        number_of_shapes = len(list_objects_names)  # 2 (3) shapes
        number_of_fusions = number_of_shapes - 1    # is 1 (2) fusions to do

        if verbose:
            print "Number of fusions to do: " + str(number_of_fusions)

        if not number_of_fusions > 0:
            raise("Not enough shapes to do a fusion!")

        # take care of the intermediate fusions
        while number_of_fusions > 1:  # if 2 fusions, the first is the -1
            # intermediate shape name
            intermediate_shape_name = name + "_minus" + str(number_of_fusions - 1)

            if verbose:
                print "Generate intermediate shape: " + intermediate_shape_name
                print "Object 1 for fusion: " + list_objects_names[0]
                print "Object 2 for fusion: " + list_objects_names[1]

            # create intermediate shape
            self.document.addObject("Part::Fuse", intermediate_shape_name)
            self.document.getObject(intermediate_shape_name).Base = self.document.getObject(list_objects_names[0])
            self.document.getObject(intermediate_shape_name).Tool = self.document.getObject(list_objects_names[1])

            self.document.recompute()

            # add it at the end of the list of shapes to fusion
            list_objects_names.append(intermediate_shape_name)

            # take away the two first elements of the list to fusion
            list_objects_names = list_objects_names[2:]

            # one less fusion to do
            number_of_fusions -= 1

        # take care of the last fusion
        if verbose:
            print "Do last fusion"
            print "Object 1 for fusion: " + list_objects_names[0]
            print "Object 2 for fusion: " + list_objects_names[1]

        self.document.addObject("Part::Fuse", name)
        self.document.getObject(name).Base = self.document.getObject(list_objects_names[0])
        self.document.getObject(name).Tool = self.document.getObject(list_objects_names[1])

        self.document.recompute()

    def perform_union_mesh(self, list_objects_names, name, verbose=False):
        """
        Perform the union of all shapes given in list_objects_names.
        The final shape is called name. Intermediate shapes are called shape_n,
        where n is an indice that indicates how many fusions left to do
        """

        number_of_shapes = len(list_objects_names)  # 2 (3) shapes
        number_of_fusions = number_of_shapes - 1    # is 1 (2) fusions to do

        if verbose:
            print "Number of fusions to do: " + str(number_of_fusions)

        if not number_of_fusions > 0:
            raise("Not enough shapes to do a fusion!")

        # take care of the intermediate fusions
        while number_of_fusions > 1:  # if 2 fusions, the first is the -1
            # intermediate shape name
            intermediate_shape_name = name + "_minus" + str(number_of_fusions - 1)

            if verbose:
                print "Generate intermediate shape: " + intermediate_shape_name
                print "Object 1 for fusion: " + list_objects_names[0]
                print "Object 2 for fusion: " + list_objects_names[1]

            # create intermediate shape
            mesh_1 = self.document.getObject(list_objects_names[0]).Mesh
            mesh_2 = self.document.getObject(list_objects_names[1]).Mesh
            mesh_interm = OpenSCADUtils.meshoptempfile('union', (mesh_1, mesh_2))
            self.document.addObject("Mesh::Feature", intermediate_shape_name)
            self.document.getObject(intermediate_shape_name).Mesh = mesh_interm

            self.document.recompute()

            # add it at the end of the list of shapes to fusion
            list_objects_names.append(intermediate_shape_name)

            # take away the two first elements of the list to fusion
            list_objects_names = list_objects_names[2:]

            # one less fusion to do
            number_of_fusions -= 1

        # take care of the last fusion
        if verbose:
            print "Do last fusion"
            print "Object 1 for fusion: " + list_objects_names[0]
            print "Object 2 for fusion: " + list_objects_names[1]

        # create intermediate shape
        mesh_1 = self.document.getObject(list_objects_names[0]).Mesh
        mesh_2 = self.document.getObject(list_objects_names[1]).Mesh
        mesh_interm = OpenSCADUtils.meshoptempfile('union', (mesh_1, mesh_2))
        self.document.addObject("Mesh::Feature", name)
        self.document.getObject(name).Mesh = mesh_interm

        self.document.recompute()

    def perform_cut(self, base, tool, name, verbose=False):
        """
        Perform the cut (substraction) of tool on base as the name object
        """

        if verbose:
            print "Doing a cut on " + base + " using " + tool

        # create intermediate shape
        self.document.addObject("Part::Cut", name)
        self.document.getObject(name).Base = self.document.getObject(base)
        self.document.getObject(name).Tool = self.document.getObject(tool)

        self.document.recompute()

    def perform_cut_mesh(self, base, tool, name, verbose=False):
        """
        Perform the cut (substraction) of tool on base as the name object
        """

        if verbose:
            print "Doing a cut on " + base + " using " + tool

        mesh_1 = self.document.getObject(base).Mesh
        mesh_2 = self.document.getObject(tool).Mesh
        mesh_interm = OpenSCADUtils.meshoptempfile('difference', (mesh_1, mesh_2))
        self.document.addObject("Mesh::Feature", name)
        self.document.getObject(name).Mesh = mesh_interm

        self.document.recompute()
