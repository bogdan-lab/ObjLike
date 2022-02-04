import numpy as np
from primitives import Point, PointCollection, Angle
from collection_2d import CircleSegment
from typing import Tuple, List

FaceType = List[Tuple[int, int, int]]


class Circle:

    def _build_mesh_in_circle(self) -> None:
        angles = Angle.convert(np.linspace(0, 2*np.pi, 7, endpoint=True))
        segments = []
        for i in range(len(angles)-1):
            segments.append(CircleSegment(angles[i], angles[i+1],
                                          self.radius, self.layer_num))
        self.points = PointCollection()
        self.faces = []
        self.outer_layer_points = []
        for seg in segments:
            for i in range(len(seg.outer_layer_points)-1):
                self.outer_layer_points.append(seg.outer_layer_points[i])
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
