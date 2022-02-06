from itertools import tee
from typing import List, Tuple, Iterable
from functools import reduce
import numpy as np
from primitives import Point, FaceCollection, Angle


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
            filter(lambda p: np.isclose(p.spherical[0], radius, atol=tol),
                   points), key=lambda p: p.spherical[1])


class Plane:
    '''Simple rectangle in XY plane centered in point (0, 0, 0)'''
    def __init__(self, width: float, height: float) -> None:
        self.description = FaceCollection()
        left_bot = Point(-width/2, -height/2, 0)
        left_top = Point(-width/2, height/2, 0)
        right_bot = Point(width/2, -height/2, 0)
        right_top = Point(width/2, height/2, 0)
        self.description.add_face(left_bot, right_bot, right_top)
        self.description.add_face(left_bot, right_top, left_top)


class Box:
    '''Simple box which diagonals crosses in (0, 0, 0)'''
    def __init__(self, width: float, height: float, depth: float) -> None:
        bot = Plane(width=width, height=depth).description.move(z=-height/2)
        top = Plane(width=width, height=depth).description.move(z=height/2)
        right = Plane(width=height, height=depth).description
        right.rotate(y=Angle(np.pi/2)).move(x=width/2)
        left = Plane(width=height, height=depth).description
        left.rotate(y=Angle(np.pi/2)).move(x=-width/2)
        front = Plane(width=width, height=height).description
        front.rotate(x=Angle(np.pi/2)).move(y=-depth/2)
        back = Plane(width=width, height=height).description
        back.rotate(x=Angle(np.pi/2)).move(y=depth/2)
        self.description = FaceCollection()
        for pl in (bot, top, right, left, front, back):
            pl.accept_transformations()
            self.description = FaceCollection.merge(self.description, pl)


class CircleSegment:
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
            description.add_face(cl, pl, cr)
            if pr:
                description.add_face(pr, cr, pl)

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
        if phi_to <= phi_from:
            raise ValueError("Incorrect range for the circcle segment.")
        self.description = FaceCollection()
        quant_num = int(np.ceil((phi_to - phi_from).value / (2*np.pi / 3)))
        angles = Angle.linspace(phi_from, phi_to, quant_num+1, endpoint=True)
        for lo, hi in pairwise(angles):
            add_descr = self._build_segment_quant(lo, hi, radius, layer_num)
            self.description = FaceCollection.merge(
                    self.description, add_descr)


class Circle:
    '''Circle in xy plane with center in (0, 0, 0)'''
    def __init__(self, radius: float, layer_num: int) -> None:
        self.description = FaceCollection()
        angles = Angle.linspace(Angle(0), Angle(2*np.pi), 7, endpoint=True)
        for lo, hi in pairwise(angles):
            add_descr = CircleSegment._build_segment_quant(
                    lo, hi, radius, layer_num)
            self.description = FaceCollection.merge(
                    self.description, add_descr)


class Tube:
    '''Tube parallel to Z axis. Tube center point is in (0, 0, 0)'''
    @staticmethod
    def _connect_layers(faces: FaceCollection, prev_layer: List[Point],
                        curr_layer: List[Point]) -> None:
        iterator = zip(pairwise(curr_layer),
                       pairwise(prev_layer))
        for (cl, cr), (pl, pr) in iterator:
            faces.add_face(cl, cr, pl)
            faces.add_face(pl, cr, pr)

    def __init__(self, radius: float, height: float, r_layer_num: int,
                 h_layer_num: int) -> None:
        angles = Angle.linspace(Angle(0), Angle(2*np.pi), 6*r_layer_num + 1,
                                endpoint=True)
        heights = np.linspace(0, height, h_layer_num+1, endpoint=True)
        point_layers = []
        for h in heights:
            point_layers.append([
                    Point.from_spherical(radius, phi, Angle(np.pi/2)).move(z=h)
                    for phi in angles])
        self.description = FaceCollection()
        for prev, curr in pairwise(point_layers):
            Tube._connect_layers(self.description, prev, curr)


class Cylinder:
    '''Simple cylinder parallel to Z axis with base circle center in (0, 0, 0)
    '''
    def __init__(self, radius: float, height: float, r_layer_num: int,
                 h_layer_num: int) -> None:
        bot_descr = Circle(radius, r_layer_num).description
        top_base = Circle(radius, r_layer_num).description.move(z=height)
        top_base.accept_transformations()
        heights = np.linspace(0, height, h_layer_num+1, endpoint=True)
        outer = _select_points_with_r(bot_descr.points, radius)
        point_layers = []
        for h in heights:
            point_layers.append([p.move(z=h) for p in _last_cycled(outer)])
        self.description = FaceCollection()
        for prev, curr in pairwise(point_layers):
            Tube._connect_layers(self.description, prev, curr)
        for descr in (bot_descr, top_base):
            self.description = FaceCollection.merge(self.description, descr)


class Cone:
    '''Simple cone parallel to Z axis with base circle center in (0, 0, 0)'''
    def __init__(self, radius: float, height: float, layer_num: int) -> None:
        bot_descr = Circle(radius, layer_num).description
        side_descr = Circle(radius, layer_num).description
        radius_height_pairs = zip(np.linspace(0, radius, layer_num+1),
                                  np.linspace(height, 0, layer_num+1))
        for r, h in radius_height_pairs:
            for p in _select_points_with_r(side_descr.points, r):
                p.move(z=h, inplace=True)
        self.description = FaceCollection.merge(side_descr, bot_descr)


class Sphere:
    '''Simple sphere with center in (0, 0, 0)'''
    @staticmethod
    def _between_points_on_sphere(p1: Point, p2: Point) -> Point:
        '''Expects that p1 and p2 are on the sphere'''
        ml = Point((p1.real[0] + p2.real[0])/2,
                   (p1.real[1] + p2.real[1])/2,
                   (p1.real[2] + p2.real[2])/2)
        return Point.from_spherical(0.5*(p1.spherical[0] + p2.spherical[0]),
                                    ml.spherical[1], ml.spherical[2])

    @staticmethod
    def _split_face(p1: Point, p2: Point, p3: Point):
        ml = Sphere._between_points_on_sphere(p1, p2)
        mr = Sphere._between_points_on_sphere(p2, p3)
        mb = Sphere._between_points_on_sphere(p1, p3)
        return ((p1, ml, mb), (ml, mr, mb), (mb, mr, p3), (ml, p2, mr))

    def __init__(self, radius: float, split_num: int) -> None:
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
        self.description = FaceCollection()
        for f in faces:
            self.description.add_face(*f)