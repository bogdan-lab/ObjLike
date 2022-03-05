from typing import List, Iterable, NamedTuple
import json
from collections import namedtuple
import numpy as np


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


class Point(NamedTuple):
    x: float = 0
    y: float = 0
    z: float = 0

    @staticmethod
    def _round(num: float) -> float:
        return round(num, 10)

    def __hash__(self) -> int:
        return hash((self._round(self.x), self._round(self.y),
                     self._round(self.z)))

    def __eq__(self, other: 'Point') -> bool:
        lhs = (self._round(self.x), self._round(self.y), self._round(self.z))
        rhs = (self._round(other.x), self._round(other.y), self._round(other.z))
        return lhs == rhs

    @property
    def r(self) -> float:
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    @property
    def phi(self) -> Angle:
        return Angle(np.arctan2(self.y, self.x))

    @property
    def theta(self) -> Angle:
        return Angle(np.arctan2(np.sqrt(self.x**2 + self.y**2), self.z))

    @classmethod
    def from_spherical(cls, r: float, phi: Angle, theta: Angle) -> 'Point':
        return cls(r * np.cos(phi.value) * np.sin(theta.value),
                   r * np.sin(phi.value) * np.sin(theta.value),
                   r * np.cos(theta.value))

    def move(self, x: float = 0, y: float = 0, z: float = 0) -> 'Point':
        '''Creates new point with coordinates shifted according to the
        arguments.
        '''
        return Point(self.x+x, self.y+y, self.z+z)

    def rotate_x(self, angle: Angle) -> 'Point':
        '''Rotates point around x axis. Rotation is performed according to
           the right hand rule. Result of rotation is returned as new point'''
        return Point(self.x,
                     np.cos(angle.value)*self.y - np.sin(angle.value)*self.z,
                     np.sin(angle.value)*self.y + np.cos(angle.value)*self.z)

    def rotate_y(self, angle: Angle) -> 'Point':
        '''Rotates point around y axis. Rotation is performed according to
           the right hand rule. Result of rotation is returned as new point'''
        return Point(np.cos(angle.value)*self.x + np.sin(angle.value)*self.z,
                     self.y,
                     -np.sin(angle.value)*self.x + np.cos(angle.value)*self.z)

    def rotate_z(self, angle: Angle) -> 'Point':
        '''Rotates point around z axis. Rotation is performed according to
           the right hand rule. Result of rotation is returned as new point'''
        return Point(np.cos(angle.value)*self.x - np.sin(angle.value)*self.y,
                     np.sin(angle.value)*self.x + np.cos(angle.value)*self.y,
                     self.z)


class Vector(NamedTuple):
    x: float = 0
    y: float = 0
    z: float = 0

    @classmethod
    def from_points(cls, start: Point, end: Point) -> 'Vector':
        return cls(end.x - start.x, end.y - start.y, end.z - start.z)

    def dot(self, other: 'Vector') -> float:
        return self.x*other.x + self.y*other.y + self.z*other.z

    def cross(self, other: 'Vector') -> 'Vector':
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)


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
            new_pc.add_point(p.move(x, y, z))
        if inplace:
            self.point_to_index = new_pc.point_to_index
        return new_pc


class FaceCollection:

    def __init__(self) -> None:
        self.points = PointCollection()
        self.faces = set()
        self.moves = {'x': 0, 'y': 0, 'z': 0}
        self.rotations = {'x': Angle(0), 'y': Angle(0), 'z': Angle(0)}

    def faced_points(self):
        '''Iterates over faces returning vertex points'''
        for f in self.faces:
            yield (self.points.get_point(f[0]),
                   self.points.get_point(f[1]),
                   self.points.get_point(f[2]))

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
            mp = p.rotate_x(self.rotations['x'])
            mp = mp.rotate_y(self.rotations['y'])
            mp = mp.rotate_z(self.rotations['z'])
            mp = mp.move(self.moves['x'], self.moves['y'], self.moves['z'])
            moved_points.add_point(mp)
        return moved_points

    def save_to_file(self, filename: str) -> None:
        '''Save current collection into given file.
        File is rewritten. File has json format with dictionary names:
            moves
            rotations
            points
            faces
        Not applied modifications are stored in moves and rotations fields.
        Points are saved in real coordinate form only
        Saving and reading operation with collection does not cause the loss
        of data
        '''
        with open(filename, 'w') as fout:
            json.dump({"moves": self.moves,
                       "rotations": {k: a.value for k, a in self.rotations.items()},
                       "points": list(self.points),
                       "faces": list(self.faces)}, fout)

    @classmethod
    def from_json_file(cls, filename: str) -> "FaceCollection":
        '''Constructs FaceCollection according to the given json file.
        It is expected that json file has the same format as described in
        save_to_file'''
        with open(filename, 'r') as fin:
            content = json.load(fin)
        result = cls()
        result.moves = content['moves']
        result.rotations = {k: Angle(v) for k, v in content['rotations'].items()}
        result.points = PointCollection()
        for p in content['points']:
            result.points.add_point(Point._make(p))
        result.faces = set(tuple(f) for f in content["faces"])
        return result

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
