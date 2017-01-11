import sys

# path to FreeCAD; I found it from:
# $ locate FreeCAD.so
FREECADPATH = '/usr/lib/freecad/lib/'


def import_fcstd(path_freecad):
    """try to import FreeCAD on path_freecad"""
    sys.path.append(path_freecad)
    try:
        import FreeCAD
    except:
        print "Could not import FreeCAD"
        print "Are you using the right path?"
