from point import Point, PointCollection
from typing import List, Tuple
from angle import Angle
import numpy as np

# TODO make Box realization through 6 planes with separate plane class


class Box:

    def __init__(self, origin: Point, width: float, height: float, depth: float
                 ) -> None:
        self.origin = origin
        self.width = width
        self.height = height
        self.depth = depth
        self.points = PointCollection()
        b0 = origin
        bw = origin.move(x=width)
        bh = origin.move(y=height)
        bd = origin.move(x=width, y=height)
        t0 = origin.move(z=depth)
        tw = origin.move(x=width, z=depth)
        th = origin.move(y=height, z=depth)
        td = origin.move(x=width, y=height, z=depth)
        self.faces = [
                (self.points.add_point(b0), self.points.add_point(bw),
                 self.points.add_point(bh)),
                (self.points.add_point(bw), self.points.add_point(bd),
                 self.points.add_point(bh)),
                (self.points.add_point(t0), self.points.add_point(th),
                 self.points.add_point(tw)),
                (self.points.add_point(td), self.points.add_point(tw),
                 self.points.add_point(th)),
                (self.points.add_point(th), self.points.add_point(t0),
                 self.points.add_point(bh)),
                (self.points.add_point(b0), self.points.add_point(bh),
                 self.points.add_point(t0)),
                (self.points.add_point(td), self.points.add_point(bw),
                 self.points.add_point(tw)),
                (self.points.add_point(td), self.points.add_point(bd),
                 self.points.add_point(bw)),
                (self.points.add_point(td), self.points.add_point(th),
                 self.points.add_point(bd)),
                (self.points.add_point(th), self.points.add_point(bh),
                 self.points.add_point(bd)),
                (self.points.add_point(bw), self.points.add_point(t0),
                 self.points.add_point(tw)),
                (self.points.add_point(bw), self.points.add_point(b0),
                 self.points.add_point(t0))
                ]

    def __eq__(self, other: 'Box') -> bool:
        return (self.origin == other.origin and
                self.width == other.width and
                self.height == other.height and
                self.points == other.points and
                self.faces == other.faces)

    def __str__(self) -> str:
        return '; '.join(("object = BOX",
                          f"origin = {self.origin}",
                          f"width = {self.width}",
                          f"height = {self.height}",
                          f"point_num = {self.points.get_points_num()}",
                          f"face_num = {len(self.faces)}"))

    def __repr__(self) -> str:
        return str(self)

    def move(self, x: float = 0, y: float = 0, z: float = 0,
             inplace: bool = False) -> 'Box':
        new_origin = self.origin.move(x, y, z, inplace)
        new_box = Box(new_origin, self.width, self.height, self.depth)
        if inplace:
            self.points = new_box.points
        return new_box

    def invert_faces(self) -> None:
        for i in range(len(self.faces)):
            self.faces[i] = (self.faces[i][2], self.faces[i][1],
                             self.faces[i][0])

    def save_to_file(self, filename: str = "box.obj_like") -> None:
        face_str = [f"s {p[0]} {p[1]} {p[2]}" for p in self.faces]
        with open(filename, 'w') as fout:
            fout.write('\n'.join(
                    self.points.get_file_str_content() + face_str))

    def get_real_points_as_tuples(self) -> List[Tuple[float, float, float]]:
        '''Retruns correctly ordered sequence of the points as tuples with
        real coordinates in it'''
        return [p.real for p in self.points.index_to_point]

# TODO make option inplace = True/False for rotation methods???
    def rotate_z(self, angle: Angle) -> 'Box':
        '''Rotate entire object around Z axis'''
        new_pc = PointCollection()
        for p in self.points.point_to_index:
            x = np.cos(angle.value)*p.real[0] - np.sin(angle.value)*p.real[1]
            y = np.sin(angle.value)*p.real[0] + np.cos(angle.value)*p.real[1]
            z = p.real[2]
            new_pc.add_point(Point(x, y, z))
        self.points = new_pc
        return self

    def rotate_y(self, angle: Angle) -> 'Box':
        '''Rotate entire object around Y axis'''
        new_pc = PointCollection()
        for p in self.points.point_to_index:
            x = np.cos(angle.value)*p.real[0] + np.sin(angle.value)*p.real[2]
            y = p.real[1]
            z = -np.sin(angle.value)*p.real[0] + np.cos(angle.value)*p.real[2]
            new_pc.add_point(Point(x, y, z))
        self.points = new_pc
        return self

    def rotate_x(self, angle: Angle) -> 'Box':
        '''Rotate entire object around X axis'''
        new_pc = PointCollection()
        for p in self.points.point_to_index:
            x = p.real[0]
            y = np.cos(angle.value)*p.real[1] - np.sin(angle.value)*p.real[2]
            z = np.sin(angle.value)*p.real[1] + np.cos(angle.value)*p.real[2]
            new_pc.add_point(Point(x, y, z))
        self.points = new_pc
        return self
# TODO Rotate method
# TODO Plot method
