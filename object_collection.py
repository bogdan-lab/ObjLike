from copy import deepcopy
from itertools import tee
from typing import List, Tuple, Iterable
from functools import reduce
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from primitives import Point, FaceCollection, Angle


# TODO delete objects from world?

# TODO replace by itertools.pairwise when it is available
def pairwise(iterable):
    '''Generates as following (1,2,3) -> (1,2), (2, 3)'''
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def _last_cycled(data: List):
    '''Generates as following (1,2,3) -> 1, 2, 3, 1'''
    for el in data:
        yield el
    yield data[0]


def _select_points_with_r(points: Iterable[Point], radius: float,
                          tol: float = 1e-8) -> Iterable[Point]:
    '''Returns all points with radius close to the given, sorted by phi angle
    '''
    return sorted(
            filter(lambda p: np.isclose(p.r, radius, atol=tol), points),
            key=lambda p: p.phi)


def _throw_if_le_zero(var, var_name):
    if var <= 0:
        raise ValueError(f"{var_name} is {var}, but should be larger than 0.")


class Object:

    def __init__(self) -> None:
        self.description = FaceCollection()

    def move(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.description.move(x, y, z)

    def rotate(self, x=Angle(0), y=Angle(0), z=Angle(0)) -> None:
        self.description.rotate(x, y, z)

    def accept_transformations(self) -> None:
        self.description.accept_transformations()

    def save_to_file(self, filename: str) -> None:
        self.description.save_to_file(filename)

    def invert(self) -> None:
        self.description.invert()

    @classmethod
    def from_json_file(cls, filename: str) -> "Object":
        result = cls()
        result.description = FaceCollection.from_json_file(filename)

    def get_max_x(self) -> float:
        return max(map(lambda p: p.x, self.description.points))

    def get_min_x(self) -> float:
        return min(map(lambda p: p.x, self.description.points))

    def get_max_y(self) -> float:
        return max(map(lambda p: p.y, self.description.points))

    def get_min_y(self) -> float:
        return min(map(lambda p: p.y, self.description.points))

    def get_max_z(self) -> float:
        return max(map(lambda p: p.z, self.description.points))

    def get_min_z(self) -> float:
        return min(map(lambda p: p.z, self.description.points))

    def plot(self) -> None:
        ''' Returns figure with plotted object on it'''
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlim3d(self.get_min_x(), self.get_max_x())
        ax.set_ylim3d(self.get_min_y(), self.get_max_y())
        ax.set_zlim3d(self.get_min_z(), self.get_max_z())
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        fig.add_axes(ax, label="main")
        faces = list(map(lambda face: (face[0], face[1], face[2]),
                         self.description.faced_points()))
        ax.add_collection3d(Poly3DCollection(faces, edgecolor="black"))
        return fig


class Plane(Object):
    '''Simple rectangle in XY plane centered in point (0, 0, 0)'''
    def __init__(self, width: float, height: float) -> None:
        _throw_if_le_zero(height, "height")
        _throw_if_le_zero(width, "width")
        super().__init__()
        self.width = width
        self.height = height
        left_bot = Point(-width/2, -height/2, 0)
        left_top = Point(-width/2, height/2, 0)
        right_bot = Point(width/2, -height/2, 0)
        right_top = Point(width/2, height/2, 0)
        self.description.add_face(left_bot, right_bot, right_top)
        self.description.add_face(left_bot, right_top, left_top)


class Box(Object):
    '''Simple box which diagonals crosses in (0, 0, 0)'''
    def __init__(self, width: float, height: float, depth: float) -> None:
        _throw_if_le_zero(depth, "depth")
        _throw_if_le_zero(height, "height")
        _throw_if_le_zero(width, "width")
        super().__init__()
        self.width = width
        self.height = height
        self.depth = depth
        bot = Plane(width=width, height=depth).description.move(z=-height/2)
        bot.invert()
        top = Plane(width=width, height=depth).description.move(z=height/2)
        right = Plane(width=height, height=depth).description
        right.rotate(y=Angle(np.pi/2)).move(x=width/2)
        left = Plane(width=height, height=depth).description
        left.rotate(y=Angle(np.pi/2)).move(x=-width/2)
        left.invert()
        front = Plane(width=width, height=height).description
        front.rotate(x=Angle(np.pi/2)).move(y=-depth/2)
        back = Plane(width=width, height=height).description
        back.rotate(x=Angle(np.pi/2)).move(y=depth/2)
        back.invert()
        for pl in (bot, top, right, left, front, back):
            pl.accept_transformations()
            self.description = FaceCollection.merge(self.description, pl)


class CircleSegment(Object):
    '''Circle segment in xy plane with center in (0, 0, 0).
    If one need to create CircleSegment(0, 2*np.pi) one should use Circle
    class instead'''
    @staticmethod
    def _layer_iterator(layer_num: int, radius: float):
        '''Generates point num on layer and layer radius as iterable'''
        for i in range(layer_num):
            yield (i + 2, (i + 1)*radius / layer_num)

    @staticmethod
    def _add_layer(description, prev: List[Point], curr: List[Point]) -> None:
        for (cl, cr), (pl, pr) in zip(pairwise(curr), pairwise(prev + [None])):
            description.add_face(cr, pl, cl)
            if pr:
                description.add_face(pl, cr, pr)

    @staticmethod
    def _build_segment_quant(phi_from: Angle, phi_to: Angle, radius: float,
                             layer_num: int) -> (FaceCollection, Tuple[Point]):
        faces = FaceCollection()
        prev_points = [Point(0, 0, 0)]
        for pts_num, r in CircleSegment._layer_iterator(layer_num, radius):
            angles = Angle.linspace(phi_from, phi_to, pts_num, endpoint=True)
            curr_points = [Point.from_spherical(r, phi, Angle(np.pi/2))
                           for phi in angles]
            CircleSegment._add_layer(faces, prev_points, curr_points)
            prev_points = curr_points
        return faces

    def __init__(self, phi_from: Angle, phi_to: Angle, radius: float,
                 layer_num: int) -> None:
        if not isinstance(layer_num, int):
            raise TypeError("layer_num should be integer")
        _throw_if_le_zero(radius, "radius")
        _throw_if_le_zero(layer_num, "layer_num")
        if phi_to <= phi_from:
            raise ValueError("Incorrect range for the circcle segment.")
        super().__init__()
        self.radius = radius
        self.phi_from = phi_from
        self.phi_to = phi_to
        self.layer_num = layer_num
        quant_num = int(np.ceil((phi_to - phi_from).value / (2*np.pi / 3)))
        angles = Angle.linspace(phi_from, phi_to, quant_num+1, endpoint=True)
        for lo, hi in pairwise(angles):
            add_descr = self._build_segment_quant(lo, hi, radius, layer_num)
            self.description = FaceCollection.merge(
                    self.description, add_descr)


class Circle(Object):
    '''Circle in xy plane with center in (0, 0, 0)'''
    def __init__(self, radius: float, layer_num: int) -> None:
        if not isinstance(layer_num, int):
            raise TypeError("layer_num should be integer")
        _throw_if_le_zero(radius, "radius")
        _throw_if_le_zero(layer_num, "layer_num")
        super().__init__()
        self.radius = radius
        self.layer_num = layer_num
        angles = Angle.linspace(Angle(0), Angle(2*np.pi), 7, endpoint=True)
        for lo, hi in pairwise(angles):
            add_descr = CircleSegment._build_segment_quant(
                    lo, hi, radius, layer_num)
            self.description = FaceCollection.merge(
                    self.description, add_descr)


class Tube(Object):
    '''Tube parallel to Z axis. Tube center point is in (0, 0, 0)'''
    @staticmethod
    def _connect_layers(faces: FaceCollection, prev_layer: List[Point],
                        curr_layer: List[Point]) -> None:
        iterator = zip(pairwise(curr_layer),
                       pairwise(prev_layer))
        for (cl, cr), (pl, pr) in iterator:
            faces.add_face(pl, cr, cl)
            faces.add_face(pr, cr, pl)

    def __init__(self, radius: float, height: float, r_layer_num: int,
                 h_layer_num: int) -> None:
        if not isinstance(r_layer_num, int):
            raise TypeError("r_layer_num should be integer")
        if not isinstance(h_layer_num, int):
            raise TypeError("h_layer_num should be integer")
        _throw_if_le_zero(radius, "radius")
        _throw_if_le_zero(height, "height")
        _throw_if_le_zero(r_layer_num, "r_layer_num")
        _throw_if_le_zero(h_layer_num, "h_layer_num")
        super().__init__()
        self.radius = radius
        self.height = height
        self.r_layer_num = r_layer_num
        self.h_layer_num = h_layer_num
        angles = Angle.linspace(Angle(0), Angle(2*np.pi), 6*r_layer_num + 1,
                                endpoint=True)
        heights = np.linspace(0, height, h_layer_num+1, endpoint=True)
        point_layers = []
        for h in heights:
            point_layers.append([
                    Point.from_spherical(radius, phi, Angle(np.pi/2)).move(z=h)
                    for phi in angles])
        for prev, curr in pairwise(point_layers):
            Tube._connect_layers(self.description, prev, curr)


class Cylinder(Object):
    '''Simple cylinder parallel to Z axis with base circle center in (0, 0, 0)
    '''
    def __init__(self, radius: float, height: float, r_layer_num: int,
                 h_layer_num: int) -> None:
        if not isinstance(r_layer_num, int):
            raise TypeError("r_layer_num should be integer")
        if not isinstance(h_layer_num, int):
            raise TypeError("h_layer_num should be integer")
        _throw_if_le_zero(radius, "radius")
        _throw_if_le_zero(height, "height")
        _throw_if_le_zero(r_layer_num, "r_layer_num")
        _throw_if_le_zero(h_layer_num, "h_layer_num")
        super().__init__()
        self.radius = radius
        self.height = height
        self.r_layer_num = r_layer_num
        self.h_layer_num = h_layer_num
        bot_descr = Circle(radius, r_layer_num).description
        bot_descr.invert()
        top_base = Circle(radius, r_layer_num).description.move(z=height)
        top_base.accept_transformations()
        heights = np.linspace(0, height, h_layer_num+1, endpoint=True)
        outer = _select_points_with_r(bot_descr.points, radius)
        point_layers = []
        for h in heights:
            point_layers.append([p.move(z=h) for p in _last_cycled(outer)])
        for prev, curr in pairwise(point_layers):
            Tube._connect_layers(self.description, prev, curr)
        for descr in (bot_descr, top_base):
            self.description = FaceCollection.merge(self.description, descr)


class ConeNoBase(Object):
    '''Simple cone parallel to Z axis with base circle center in (0, 0, 0)
        but without base plane'''
    def __init__(self, radius: float, height: float, layer_num: int) -> None:
        if not isinstance(layer_num, int):
            raise TypeError("layer_num should be integer")
        _throw_if_le_zero(radius, "radius")
        _throw_if_le_zero(height, "height")
        _throw_if_le_zero(layer_num, "layer_num")
        super().__init__()
        self.radius = radius
        self.height = height
        self.layer_num = layer_num
        side_descr = Circle(radius, layer_num).description
        for p1, p2, p3 in side_descr.faced_points():
            self.description.add_face(p1.move(z=(radius - p1.r)/radius*height),
                                      p2.move(z=(radius - p2.r)/radius*height),
                                      p3.move(z=(radius - p3.r)/radius*height))


class Cone(Object):
    '''Simple cone parallel to Z axis with base circle center in (0, 0, 0)'''
    def __init__(self, radius: float, height: float, layer_num: int) -> None:
        if not isinstance(layer_num, int):
            raise TypeError("layer_num should be integer")
        _throw_if_le_zero(radius, "radius")
        _throw_if_le_zero(height, "height")
        _throw_if_le_zero(layer_num, "layer_num")
        super().__init__()
        self.radius = radius
        self.height = height
        self.layer_num = layer_num
        bot_descr = Circle(radius, layer_num).description
        bot_descr.invert()
        side_descr = ConeNoBase(radius, height, layer_num).description
        self.description = FaceCollection.merge(side_descr, bot_descr)


class Sphere(Object):
    '''Simple sphere with center in (0, 0, 0)'''
    @staticmethod
    def _between_points_on_sphere(p1: Point, p2: Point) -> Point:
        '''Expects that p1 and p2 are on the sphere'''
        ml = Point((p1.x + p2.x)/2,
                   (p1.y + p2.y)/2,
                   (p1.z + p2.z)/2)
        return Point.from_spherical(0.5*(p1.r + p2.r), ml.phi, ml.theta)

    @staticmethod
    def _split_face(p1: Point, p2: Point, p3: Point):
        ml = Sphere._between_points_on_sphere(p1, p2)
        mr = Sphere._between_points_on_sphere(p2, p3)
        mb = Sphere._between_points_on_sphere(p1, p3)
        return ((p1, ml, mb), (ml, mr, mb), (mb, mr, p3), (ml, p2, mr))

    def __init__(self, radius: float, split_num: int) -> None:
        if not isinstance(split_num, int):
            raise TypeError("split_num should be an integer")
        _throw_if_le_zero(split_num, "split_num")
        _throw_if_le_zero(radius, "radius")
        super().__init__()
        self.radius = radius
        self.split_num = split_num
        top = Point(0, 0, radius)
        xp = Point(radius, 0, 0)
        yp = Point(0, radius, 0)
        xm = Point(-radius, 0, 0)
        ym = Point(0, -radius, 0)
        bot = Point(0, 0, -radius)
        faces = ((yp, top, xp), (xm, top, yp), (ym, top, xm), (xp, top, ym),
                 (xp, bot, yp), (yp, bot, xm), (xm, bot, ym), (ym, bot, xp))
        for _ in range(split_num-1):
            faces = reduce(lambda initial, f: initial + Sphere._split_face(*f),
                           faces, tuple())
        for f in faces:
            self.description.add_face(*f)


class World(Object):
    '''Aggregation of different objects'''
    def add_object(self, obj: Object) -> None:
        '''Adds object to the world'''
        if (any(x != 0 for x in self.description.moves.values()) or
            any(x != Angle(0) for x in self.description.rotations.values())):
            raise RuntimeError("Cannot add object to the world with not"
                               "accepted transformations")
        if not isinstance(obj, Object):
            raise TypeError("Only object can be added to the world")
        input_description = FaceCollection()
        input_description.points = obj.description.get_transformed_points()
        input_description.faces = deepcopy(obj.description.faces)
        self.description = FaceCollection.merge(self.description,
                                                input_description)
