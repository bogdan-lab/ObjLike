import numpy as np
from primitives import Point
from circle import Circle


def test_circle_creation_1_layer():
    origin = Point(1, 2, 3)
    circle = Circle(origin, radius=5, layer_num=1)
    assert circle.origin == origin
    assert circle.points.get_points_num() == 7
    assert len(circle.faces) == 6
    out_l = circle.outer_layer_points
    assert len(out_l) == 6
    assert all([np.isclose(p.spherical[0], circle.radius) for p in out_l])
    assert all([out_l[i].spherical[1] < out_l[i+1].spherical[1]
                for i in range(len(out_l)-1)])


def test_circle_creation_2_layer():
    origin = Point(1, 2, 3)
    circle = Circle(origin, radius=5, layer_num=2)
    assert circle.origin == origin
    assert circle.points.get_points_num() == 19
    assert len(circle.faces) == 24
    out_l = circle.outer_layer_points
    assert len(out_l) == 12
    assert all([np.isclose(p.spherical[0], circle.radius) for p in out_l])
    assert all([out_l[i].spherical[1] < out_l[i+1].spherical[1]
                for i in range(len(out_l)-1)])


def test_circle_creation_3_layer():
    origin = Point(1, 2, 3)
    circle = Circle(origin, radius=5, layer_num=3)
    assert circle.origin == origin
    assert circle.points.get_points_num() == 37
    assert len(circle.faces) == 54
    out_l = circle.outer_layer_points
    assert len(out_l) == 18
    assert all([np.isclose(p.spherical[0], circle.radius) for p in out_l])
    assert all([out_l[i].spherical[1] < out_l[i+1].spherical[1]
                for i in range(len(out_l)-1)])
