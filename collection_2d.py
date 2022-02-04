from itertools import zip_longest, tee
from typing import List
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

    @staticmethod
    def _layer_parameters(layer_num: int, radius: float):
        '''Generates point num on layer and layer radius as iterable'''
        for i in range(layer_num):
            yield (i + 2, (i + 1)*radius / layer_num)

    def _connect_layers(self, prev: List[Point], curr: List[Point]) -> None:
        for (cl, cr), (pl, pr) in zip(pairwise(curr), pairwise(prev + [None])):
            self.description.add_face(cl, pl, cr)
            if pr:
                self.description.add_face(pr, cr, pl)

    def _build_mesh_in_segment(self) -> None:
        self.description = FaceCollection()
        prev_layer_points = [Point(0, 0, 0)]
        for pts_num, r in self._layer_parameters(self.layer_num, self.radius):
            angles = Angle.linspace(self.phi_from, self.phi_to, pts_num,
                                    endpoint=True)
            curr_layer_points = [
                    Point.from_spherical(r, phi, Angle(np.pi/2))
                    for phi in angles]
            self._connect_layers(prev_layer_points, curr_layer_points)
            prev_layer_points = curr_layer_points
        self.outer_layer_points = tuple(curr_layer_points)

    def __init__(self, phi_from: Angle, phi_to: Angle, radius: float,
                 layer_num: int) -> None:
        self.phi_from = phi_from
        self.phi_to = phi_to
        self.radius = radius
        self.layer_num = layer_num
        self._build_mesh_in_segment()




# TODO move here Circle CircleSegment
