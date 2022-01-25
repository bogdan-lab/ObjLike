import numpy as np
from angle import Angle
from point import Point
from circle import CircleSegment, Circle


def test_segment_creation_1_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/3),
                        radius=5, layer_num=1)
    assert seg.r_step == seg.radius
    assert seg.r_step == 5
    assert seg.points.get_points_num() == 3
    assert len(seg.faces) == 1
    assert seg.faces[0] == (0, 1, 2)
    out_l = seg.outer_layer_points
    assert len(out_l) == 2
    assert all([np.isclose(p.spherical[0], seg.radius) for p in out_l])
    assert all([out_l[i].spherical[1] < out_l[i+1].spherical[1]
                for i in range(len(out_l)-1)])


def test_segment_creation_2_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/3),
                        radius=4, layer_num=2)
    assert seg.r_step == 2
    assert seg.points.get_points_num() == 6
    assert len(seg.faces) == 4
    out_l = seg.outer_layer_points
    assert len(out_l) == 3
    assert all([np.isclose(p.spherical[0], seg.radius) for p in out_l])
    assert all([out_l[i].spherical[1] < out_l[i+1].spherical[1]
                for i in range(len(out_l)-1)])


def test_segment_creation_3_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/2),
                        radius=9, layer_num=3)
    assert seg.r_step == 3
    assert seg.points.get_points_num() == 10
    assert len(seg.faces) == 9
    out_l = seg.outer_layer_points
    assert len(out_l) == 4
    assert all([np.isclose(p.spherical[0], seg.radius) for p in out_l])
    assert all([out_l[i].spherical[1] < out_l[i+1].spherical[1]
                for i in range(len(out_l)-1)])


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
