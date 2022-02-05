from itertools import tee
from typing import List, Tuple
import numpy as np
from primitives import Point, FaceCollection, Angle


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


# TODO replace by itertools.pairwise when it is available
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class CircleSegment:
    '''Circle segment in xy plane with center in (0, 0, 0).
    If one need to create CircleSegment(0, 2*np.pi) one should use Circle
    class instead
    '''

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
        return faces, tuple(curr_points)

    def __init__(self, phi_from: Angle, phi_to: Angle, radius: float,
                 layer_num: int) -> None:
        if phi_to <= phi_from:
            raise ValueError("Incorrect range for the circcle segment.")
        self.phi_from = phi_from
        self.phi_to = phi_to
        self.radius = radius
        self.layer_num = layer_num
        self.description = FaceCollection()
        self.outer_layer_points = tuple()
        quant_num = int(np.ceil((phi_to - phi_from).value / (2*np.pi / 3)))
        angles = Angle.linspace(phi_from, phi_to, quant_num+1, endpoint=True)
        for lo, hi in pairwise(angles):
            add_descr, add_out = self._build_segment_quant(
                    lo, hi, radius, layer_num)
            self.description = FaceCollection.merge(
                    self.description, add_descr)
            self.outer_layer_points += tuple(p for p in add_out
                                             if p not in
                                             self.outer_layer_points)


class Circle:
    '''Circle in xy plane with center in (0, 0, 0)'''

    def __init__(self, radius: float, layer_num: int) -> None:
        self.radius = radius
        self.layer_num = layer_num
        self.description = FaceCollection()
        self.outer_layer_points = tuple()
        angles = Angle.linspace(Angle(0), Angle(2*np.pi), 7, endpoint=True)
        for lo, hi in pairwise(angles):
            add_descr, add_out = CircleSegment._build_segment_quant(
                    lo, hi, radius, layer_num)
            self.description = FaceCollection.merge(
                    self.description, add_descr)
            self.outer_layer_points += tuple(p for p in add_out
                                             if p not in
                                             self.outer_layer_points)


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
