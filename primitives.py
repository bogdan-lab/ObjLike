import numpy as np
from typing import Tuple, List, Iterable


class Angle:
    '''Simple class that guaranties that stored value will be between (0, 2*pi)
    '''
    def __init__(self, value: float) -> None:
        value = value - int(value/(2*np.pi))*2*np.pi
        if value < 0:
            value += 2*np.pi
        self.value = value

    def __eq__(self, other: 'Angle') -> bool:
        return self.value == other.value

    def __lt__(self, other: 'Angle') -> bool:
        return self.value < other.value

    def __le__(self, other: 'Angle') -> bool:
        return self.value <= other.value

    def __gt__(self, other: 'Angle') -> bool:
        return self.value > other.value

    def __ge__(self, other: 'Angle') -> bool:
        return self.value >= other.value

    def __add__(self, other: 'Angle') -> bool:
        return Angle(self.value + other.value)

    def __sub__(self, other: 'Angle') -> bool:
        return Angle(self.value - other.value)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def convert(data: Iterable) -> List['Angle']:
        return [Angle(val) for val in data]

    @staticmethod
    def linspace(lo: 'Angle', hi: 'Angle', pt_num: int,
                 endpoint=True) -> List['Angle']:
        if hi.value != 0 and lo.value > hi.value:
            raise RuntimeError("Incorrect boundaries for creating set")
        top_val = hi.value
        if hi.value == 0 and lo.value >= 0:
            top_val = 2*np.pi
        return Angle.convert(np.linspace(lo.value, top_val, pt_num,
                                         endpoint=endpoint))


SphericalPointTuple = Tuple[float, Angle, Angle]
RealPointTuple = Tuple[float, float, float]


class Point:

    @staticmethod
    def convert_spherical_point_to_real(point: SphericalPointTuple
                                        ) -> RealPointTuple:
        '''spher_point = [r, phi, theta]'''
        return (point[0] * np.cos(point[1].value) * np.sin(point[2].value),
                point[0] * np.sin(point[1].value) * np.sin(point[2].value),
                point[0] * np.cos(point[2].value))

    @staticmethod
    def convert_real_point_to_spherical(point: RealPointTuple
                                        ) -> SphericalPointTuple:
        return (np.sqrt(point[0]**2 + point[1]**2 + point[2]**2),
                Angle(np.arctan2(point[1], point[0])),
                Angle(np.arctan2(np.sqrt(point[0]**2 + point[1]**2), point[2]))
                )

    def __init__(self, x: float, y: float, z: float) -> None:
        self.real = (x, y, z)
        self.spherical = Point.convert_real_point_to_spherical(self.real)

    def __eq__(self, other: 'Point') -> bool:
        return self.real == other.real

    def __hash__(self) -> int:
        return hash(self.real)

    def __str__(self) -> str:
        return f"({self.real[0]}, {self.real[1]}, {self.real[2]})"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def from_spherical(cls, r: float, phi: Angle, theta: Angle) -> 'Point':
        real = Point.convert_spherical_point_to_real((r, phi, theta))
        point = cls(real[0], real[1], real[2])
        return point

    def move(self, x: float = 0, y: float = 0, z: float = 0,
             inplace: bool = False) -> 'Point':
        new_point = Point(self.real[0] + x, self.real[1] + y, self.real[2] + z)
        if inplace:
            self.real = new_point.real
            self.spherical = new_point.spherical
        return new_point

    def rotate_x(self, angle: Angle, inplace: bool = False) -> 'Point':
        '''Rotates point around x axis. Rotation is performed according to
           the right hand rule
        '''
        x = self.real[0]
        y = np.cos(angle.value)*self.real[1] - np.sin(angle.value)*self.real[2]
        z = np.sin(angle.value)*self.real[1] + np.cos(angle.value)*self.real[2]
        new_point = Point(x, y, z)
        if inplace:
            self.real = new_point.real
            self.spherical = new_point.spherical
        return new_point

    def rotate_y(self, angle: Angle, inplace: bool = False) -> 'Point':
        '''Rotates point around y axis. Rotation is performed according to
           the right hand rule
        '''
        x = np.cos(angle.value)*self.real[0] + np.sin(angle.value)*self.real[2]
        y = self.real[1]
        z = (-np.sin(angle.value)*self.real[0]
             + np.cos(angle.value)*self.real[2])
        new_point = Point(x, y, z)
        if inplace:
            self.real = new_point.real
            self.spherical = new_point.spherical
        return new_point

    def rotate_z(self, angle: Angle, inplace: bool = False) -> 'Point':
        '''Rotates point around z axis. Rotation is performed according to
           the right hand rule
        '''
        x = np.cos(angle.value)*self.real[0] - np.sin(angle.value)*self.real[1]
        y = np.sin(angle.value)*self.real[0] + np.cos(angle.value)*self.real[1]
        z = self.real[2]
        new_point = Point(x, y, z)
        if inplace:
            self.real = new_point.real
            self.spherical = new_point.spherical
        return new_point

    def get_real_string(self) -> str:
        return f"{self.real[0]} {self.real[1]} {self.real[2]}"


class PointCollection:

    def __init__(self) -> None:
        self.next_index = 0
        self.point_to_index = {}

    def __eq__(self, other: 'PointCollection') -> bool:
        return (self.next_index == other.next_index and
                self.point_to_index == other.point_to_index)

    def __str__(self) -> str:
        return str(self.point_to_index)

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        return iter(self.point_to_index)

    def __len__(self):
        return len(self.point_to_index)

    def add_point(self, p: Point) -> int:
        if not isinstance(p, Point):
            raise TypeError("PointCollection should contain only Points")
        if p not in self.point_to_index:
            self.point_to_index[p] = self.next_index
            self.next_index += 1
        return self.point_to_index[p]

    def get_point(self, index: int) -> Point:
        return list(self.point_to_index)[index]

    def move(self, x: float = 0, y: float = 0, z: float = 0,
             inplace: bool = False) -> 'PointCollection':
        new_pc = PointCollection()
        for p in self.point_to_index:
            new_pc.add_point(p.move(x, y, z, inplace=False))
        if inplace:
            self.point_to_index = new_pc.point_to_index
        return new_pc

    def get_file_str_content(self) -> List[str]:
        return [f"p {p.get_real_string()}" for p in self.point_to_index]


class FaceCollection:

    def __init__(self) -> None:
        self.points = PointCollection()
        self.faces = set()
        self.moves = {'x': 0, 'y': 0, 'z': 0}
        self.rotations = {'x': Angle(0), 'y': Angle(0), 'z': Angle(0)}

    def add_face(self, p1: Point, p2: Point, p3: Point) -> None:
        self.faces.add((self.points.add_point(p1),
                        self.points.add_point(p2),
                        self.points.add_point(p3)))

    def move(self, x: float = 0, y: float = 0,
             z: float = 0) -> 'FaceCollection':
        self.moves['x'] += x
        self.moves['y'] += y
        self.moves['z'] += z
        return self

    def rotate(self, x: Angle = Angle(0), y: Angle = Angle(0),
               z: Angle = Angle(0)) -> 'FaceCollection':
        self.rotations['x'] += x
        self.rotations['y'] += y
        self.rotations['z'] += z
        return self

    def accept_transformations(self) -> None:
        '''This method applies saved transformations into current
            points collection. After this it clears all queued transformations
            and instance continue its existance as if transformed points are
            its self points. Note that all rotations are done before all
            move transformations. Also rotations are done in the following
            order x-> y -> z
        '''
        self.points = self.get_transformed_points()
        self.moves = {'x': 0, 'y': 0, 'z': 0}
        self.rotations = {'x': Angle(0), 'y': Angle(0), 'z': Angle(0)}

    def get_transformed_points(self) -> PointCollection:
        '''Returns transformed PointCollection without affecting instance
        state. Transformed points order is the same as initial points order.
        Note that all rotations are done before all move transformations.
        Also rotations are done in the following order x-> y -> z
        '''
        moved_points = PointCollection()
        for p in self.points.point_to_index:
            mp = p.rotate_x(self.rotations['x'], inplace=False)
            mp.rotate_y(self.rotations['y'], inplace=True)
            mp.rotate_z(self.rotations['z'], inplace=True)
            mp.move(x=self.moves['x'], y=self.moves['y'], z=self.moves['z'],
                    inplace=True)
            moved_points.add_point(mp)
        return moved_points

    def save_to_file(self, filename: str) -> None:
        '''Save current collection into given file.
        File is rewritten. Two groups of point collections are saved:
        self object points (sp) and transformed points (wp).
        '''
        obj_pts_str = [f"sp {p.real[0]} {p.real[1]} {p.real[2]}"
                       for p in self.points.point_to_index]
        face_str = [f"s {fc[0]} {fc[1]} {fc[2]}" for fc in self.faces]
        moved_points = self.get_transformed_points()
        mvd_pts_str = [f"wp {p.real[0]} {p.real[1]} {p.real[2]}"
                       for p in moved_points.point_to_index]
        with open(filename, 'w') as fout:
            fout.write('\n'.join(obj_pts_str + mvd_pts_str + face_str))

    @staticmethod
    def merge(lhs: 'FaceCollection',
              rhs: 'FaceCollection') -> 'FaceCollection':
        '''Creates FaceCollection which contains all faces from both
        collections. Both input collections should have same transformation
        settings.
        '''
        if lhs.moves != rhs.moves:
            raise ValueError(f"Cannot merge collections with different move"
                             "transformations: "
                             "lhs = {lhs.moves}, rhs = {rhs.moves}")
        if lhs.rotations != rhs.rotations:
            raise ValueError(f"Cannot merge collections with different"
                             "rotateions: lhs = {lhs.rotations}, "
                             "rhs = {rhs.rotations}")
        new_col = FaceCollection()
        for f in lhs.faces:
            new_col.add_face(lhs.points.get_point(f[0]),
                             lhs.points.get_point(f[1]),
                             lhs.points.get_point(f[2]))
        for f in rhs.faces:
            new_col.add_face(rhs.points.get_point(f[0]),
                             rhs.points.get_point(f[1]),
                             rhs.points.get_point(f[2]))
        new_col.moves = lhs.moves
        new_col.rotations = lhs.rotations
        return new_col
