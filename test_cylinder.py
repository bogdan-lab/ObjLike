from cylinder import Cylinder
from point import Point
import numpy as np


def test_cylinder_creation():
    radius = 5
    height = 10
    test = Cylinder(Point(0, 0, 0), radius, height, layer_num=1)
    assert len(test.points.point_to_index) == 14
    assert (sum([np.isclose(p.real[2], height)
                 for p in test.points.point_to_index]) == 7)
    assert (sum([np.isclose(p.real[2], 0)
                 for p in test.points.point_to_index]) == 7)
    radiuses = [p.spherical[0] for p in test.points.point_to_index]
    assert sum(np.isclose(radiuses, radius)) == 6
    assert sum(np.isclose(radiuses, np.sqrt(radius**2+height**2))) == 6
    assert len(test.faces) == 24
    side_face_counter = 0
    for f in test.faces:
        top_count = sum([np.isclose(test.points.get_point(pid).real[2], height)
                        for pid in f])
        bot_count = sum([np.isclose(test.points.get_point(pid).real[2], 0)
                        for pid in f])
        if top_count == 2 or bot_count == 2:
            side_face_counter += 1
    assert side_face_counter == 12
