import numpy as np
from typing import Tuple, List
from angle import Angle

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

    def get_points_num(self) -> int:
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
