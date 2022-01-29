
import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from point import Point
from box import Box
from angle import Angle
from circle import CircleSegment, Circle
from cylinder import Cylinder


# List of elements I want to be able to create:
# 1) Box - using triangles only
# 1.5) ??? wall
# 2) Sphere - using triangle (in future smooth)
# 3) Cylinder - triangle only
# 4) Cone


# =============================================================================
# Formet of the resulting file will be
# '#' - reserved for line comments
# 'p' - marks point coordinates (x, y, z) splitted by space
# 's' - surface record. It has 3 integer values, representing points
#       defined above. Indexes are separated by space. All surfaces are
#       triangles - there should alwasy be 3 indexes
# alwasy be 3 indexes
# File:
# #Comment
# p xxxx yyyy zzzz
# p xxxx yyyy zzzz
# p xxxx yyyy zzzz
# s i1 i2 i3
# s i1 i2 i3
# s i1 i2 i3
# =============================================================================

DEFAULT_OUTPUT_FILE = "element.obj_like"


# If I make this a plymorphic method it can be done faster than linear search!
def get_object_boundaries(points):
    xmin = np.inf
    xmax = -np.inf
    ymin = np.inf
    ymax = -np.inf
    zmin = np.inf
    zmax = -np.inf
    for p in points:
        xmin = min(xmin, p[0].real)
        xmax = max(xmax, p[0])
        ymin = min(ymin, p[1])
        ymax = max(ymax, p[1])
        zmin = min(zmin, p[2])
        zmax = max(zmax, p[2])
    return {"xlim": (xmin, xmax), "ylim": (ymin, ymax), "zlim": (zmin, zmax)}


def get_polygon_list(points, faces):
    return [[points[f[0]], points[f[1]], points[f[2]]] for f in faces]


def plot_result(points, faces):
    fig = plt.figure()
    ax = Axes3D(fig)
    bounds = get_object_boundaries(points)
    ax.set_xlim3d(bounds["xlim"])
    ax.set_ylim3d(bounds["ylim"])
    ax.set_zlim3d(bounds["zlim"])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    fig.add_axes(ax, label="main")
    ax.add_collection3d(
            Poly3DCollection(
                    get_polygon_list(points, faces),
                    edgecolor="black"
            )
    )
    plt.show()


def reverse_face_orientation(faces):
    for i in range(len(faces)):
        faces[i] = (faces[i][2], faces[i][1], faces[i][0])


def create_box(args):
    box = Box(origin=Point(args.x0, args.y0, args.z0),
              width=args.width, height=args.height, depth=args.depth)
    if args.inner_orientation:
        box.invert_faces()
    if not args.no_plot:
        plot_result(box.get_real_points_as_tuples(), box.faces)
    box.save_to_file(args.output_file)


def create_segment(args):
    # TODO add effect for origin
    segment = CircleSegment(Angle(args.phi_lo), Angle(args.phi_hi),
                            args.radius, args.layer_num)
    # TODO orientation effect
    if not args.no_plot:
        plot_result(segment.get_real_points_as_tuples(), segment.faces)
    # TODO save into file


def create_circle(args):
    circle = Circle(origin=Point(args.x0, args.y0, args.z0),
                    radius=args.radius, layer_num=args.layer_num)
    if not args.no_plot:
        plot_result(circle.get_real_points_as_tuples(), circle.faces)


def create_cylinder(args):
    cylinder = Cylinder(origin=Point(args.x0, args.y0, args.z0),
                        radius=args.radius, height=args.height,
                        layer_num=args.layer_num)
    if not args.no_plot:
        plot_result(cylinder.get_real_points_as_tuples(), cylinder.faces)


def add_box_parser(subparsers, parent_prasers):
    box_parser = subparsers.add_parser(
            "box",
            parents=parent_prasers,
            help="General box element",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
    box_parser.add_argument('-w', '--width', type=float, required=True,
                            help="box width along X coordinate")
    box_parser.add_argument('-a', '--height', type=float, required=True,
                            help="box height along Y coordinate")
    box_parser.add_argument('-d', '--depth', type=float, required=True,
                            help="box depth along Z coordinate")
    box_parser.set_defaults(callback=create_box)


def add_segment_parser(subparsers, parent_parsers):
    segment_parser = subparsers.add_parser(
            "segment",
            parents=parent_parsers,
            help="Circle segment element",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
    segment_parser.add_argument('-lo', '--phi_lo', type=float, required=True,
                                help="lower angle boundari of the segment")
    segment_parser.add_argument('-hi', '--phi_hi', type=float, required=True,
                                help="higher angle boundari of the segment")
    segment_parser.add_argument('-r', '--radius', type=float, required=True,
                                help='Circle radius for which segment will'
                                'be build')
    segment_parser.add_argument('-ln', '--layer_num', type=int, required=True,
                                help='Number of mesh layers in the segment')
    # TODO add some checker since layer_num should be larger than 0
    segment_parser.set_defaults(callback=create_segment)


def add_circle_parser(subparsers, parent_parsers):
    circle_parser = subparsers.add_parser(
            "circle",
            parents=parent_parsers,
            help="Basic circle element",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
    circle_parser.add_argument('-r', '--radius', type=float, required=True,
                               help="Circle radius")
    circle_parser.add_argument('-ln', '--layer_num', type=int, required=True,
                               help='Number of mesh layers in the circle')
    circle_parser.set_defaults(callback=create_circle)


def add_cylinder_parser(subparsers, parent_parsers):
    cylinder_parser = subparsers.add_parser(
            "cylinder",
            parents=parent_parsers,
            help="Basic cylinder element",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
    cylinder_parser.add_argument('-r', '--radius', type=float, required=True,
                                 help="Radius of the cylinder bases")
    cylinder_parser.add_argument('-t', '--height', type=float, required=True,
                                 help="Cylinder height")
    cylinder_parser.add_argument('-ln', '--layer_num', type=int, required=True,
                                 help="Number of mesh layers in the"
                                 "cylinder bases")
    cylinder_parser.set_defaults(callback=create_cylinder)


# TODO default argument of filename has to be for each element unique
def setup_parser(parser):
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
              '-o',
              '--output_file',
              required=False,
              default=DEFAULT_OUTPUT_FILE,
              help="File name into which the resulting element will be saved"
    )
    parent_parser.add_argument('-x0', '--x0', type=float, required=True,
                               help="X coordinate of the origin")
    parent_parser.add_argument('-y0', '--y0', type=float, required=True,
                               help="Y coordinate of the origin")
    parent_parser.add_argument('-z0', '--z0', type=float, required=True,
                               help="Z coordinate of the origin")
    parent_parser.add_argument(
            '--no_plot',
            action='store_true',
            default=False,
            help="Turns off plotting of the created element"
    )
    parent_parser.add_argument(
            '--inner_orientation',
            action='store_true',
            default=False,
            help="If set, polygon normals wil be directed inside the element"
    )

    subparsers = parser.add_subparsers(
            help="type of the element which will be plotted")
    add_box_parser(subparsers, [parent_parser])
    add_segment_parser(subparsers, [parent_parser])
    add_circle_parser(subparsers, [parent_parser])
    add_cylinder_parser(subparsers, [parent_parser])


def main():
    parser = argparse.ArgumentParser(
        prog="Image element creator CLI",
        description="Tool for creating sort of *.obj files which can be used"
        " as input in current path tracer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)
    pass


if __name__ == "__main__":
    main()
