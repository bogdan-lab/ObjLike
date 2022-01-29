from cylinder import Cylinder
from point import Point
import numpy as np


def test_cylinder_creation():
    radius = 5
    height = 10
    test = Cylinder(Point(0, 0, 0), radius, height, layer_num=1)
    assert len(test.points.point_to_index) == 14
    assert (sum([p.real[2] == height
                 for p in test.points.point_to_index]) == 7)
    assert (sum([p.real[2] == 0
                 for p in test.points.point_to_index]) == 7)
    radiuses = [p.spherical[0] for p in test.points.point_to_index]
    assert sum(np.isclose(radiuses, radius)) == 12
