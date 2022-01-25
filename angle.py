import numpy as np
from typing import Iterable, List


class Angle:
    '''Simple class that guaranties that stored value will be between
    (-2*pi, 2*pi)
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
