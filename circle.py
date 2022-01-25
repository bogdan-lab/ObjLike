import numpy as np
from point import Point, PointCollection
from angle import Angle
from typing import Tuple, List

FaceType = List[Tuple[int, int, int]]


class CircleSegment:
    '''Describes circle segment
    The circle is places in xy plane, with normal (0, 0, 1)
    '''

    @staticmethod
    def _connect_lyers(prev: List[Point], curr: List[Point],
                       pc: PointCollection, faces: FaceType) -> None:
        pi = 0
        for ci in range(len(curr)-1):
            faces.append((pc.add_point(curr[ci]),
                          pc.add_point(prev[pi]),
                          pc.add_point(curr[ci+1])))
            if pi + 1 < len(prev):
                faces.append((pc.add_point(prev[pi+1]),
                              pc.add_point(curr[ci+1]),
                              pc.add_point(prev[pi])))
            pi += 1

    def _build_mesh_in_segment(self) -> None:
        self.points = PointCollection()
        self.faces = []
        prev_layer_points = [Point(0, 0, 0)]
        for li in range(self.layer_num):
            pts_num = li + 2
            r = (li + 1) * self.r_step
            angles = Angle.linspace(self.phi_from, self.phi_to, pts_num,
                                    endpoint=True)
            curr_layer_points = [
                    Point.from_spherical(r, phi, Angle(np.pi/2))
                    for phi in angles]
            CircleSegment._connect_lyers(prev_layer_points, curr_layer_points,
                                         self.points, self.faces)
            prev_layer_points = curr_layer_points

    def __init__(self, phi_from: Angle, phi_to: Angle, radius: float,
                 layer_num: int) -> None:
        self.phi_from = phi_from
        self.phi_to = phi_to
        self.radius = radius
        self.r_step = radius / layer_num
        self.layer_num = layer_num
        self._build_mesh_in_segment()

    def get_real_points_as_tuples(self) -> List[Tuple[float, float, float]]:
        '''Retruns correctly ordered sequence of the points as tuples with
        real coordinates in it'''
        return [p.real for p in self.points.index_to_point]

# TODO Add rotation methods here!
# TODO save to file method
# TODO move method


class Circle:

    def _build_mesh_in_circle(self) -> None:
        angles = Angle.convert(np.linspace(0, 2*np.pi, 7, endpoint=True))
        segments = []
        for i in range(len(angles)-1):
            segments.append(CircleSegment(angles[i], angles[i+1],
                                          self.radius, self.layer_num))
        self.points = PointCollection()
        self.faces = []
        for seg in segments:
            for seg_face in seg.faces:
                self.faces.append(
                  ((self.points.add_point(seg.points.get_point(seg_face[0]))),
                   (self.points.add_point(seg.points.get_point(seg_face[1]))),
                   (self.points.add_point(seg.points.get_point(seg_face[2])))))

    def __init__(self, origin: Point, radius: float, layer_num: int) -> None:
        '''Creates Circle

        Internally circle with normal equal to (0, 0, 1) will be created
        The resulted points will be rotated only in getters
        '''
        self.origin = origin
        self.radius = radius
        self.layer_num = layer_num
        self._build_mesh_in_circle()

    def get_real_points_as_tuples(self) -> List[Tuple[float, float, float]]:
        '''Retruns correctly ordered sequence of the points as tuples with
        real coordinates in it'''
        return [p.real for p in self.points.index_to_point]
# TODO save in file
# TODO rotate method
# TODO move method
