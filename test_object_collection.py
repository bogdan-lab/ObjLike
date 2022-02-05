import numpy as np
from collection_2d import CircleSegment, Circle, Tube, Cylinder, Cone
from primitives import Angle


def test_segment_creation_1_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/3),
                        radius=5, layer_num=1)
    assert len(seg.description.faces) == 1
    assert (0, 1, 2) in seg.description.faces
    assert seg.description.points.get_points_num() == 3


def test_segment_creation_2_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/3),
                        radius=4, layer_num=2)
    assert len(seg.description.faces) == 4
    assert seg.description.points.get_points_num() == 6


def test_segment_creation_3_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/2),
                        radius=9, layer_num=3)
    assert len(seg.description.faces) == 9
    assert seg.description.points.get_points_num() == 10


def test_create_circle_from_segment_1_layer():
    circle = Circle(radius=5, layer_num=1)
    assert len(circle.description.faces) == 6
    assert circle.description.points.get_points_num() == 7


def test_create_circle_from_segment_3_layer():
    circle = Circle(radius=9, layer_num=3)
    assert len(circle.description.faces) == 54
    assert circle.description.points.get_points_num() == 37


def test_tube_creation_1_layer():
    tube = Tube(radius=15, height=5, r_layer_num=1, h_layer_num=1)
    assert tube.description.points.get_points_num() == 12
    assert len(tube.description.faces) == 12
    assert sum(np.isclose(p.real[2], 0)
               for p in tube.description.points.point_to_index) == 6
    assert sum(np.isclose(p.real[2], 5)
               for p in tube.description.points.point_to_index) == 6


def test_tube_creation_3_layer():
    tube = Tube(radius=15, height=9, h_layer_num=3, r_layer_num=1)
    assert len(tube.description.faces) == 36
    assert tube.description.points.get_points_num() == 24
    assert sum(np.isclose(p.real[2], 0)
               for p in tube.description.points.point_to_index) == 6
    assert sum(np.isclose(p.real[2], 3)
               for p in tube.description.points.point_to_index) == 6
    assert sum(np.isclose(p.real[2], 6)
               for p in tube.description.points.point_to_index) == 6
    assert sum(np.isclose(p.real[2], 9)
               for p in tube.description.points.point_to_index) == 6


def test_tube_creation_2_layer():
    tube = Tube(radius=15, height=6, h_layer_num=2, r_layer_num=2)
    assert len(tube.description.faces) == 48
    assert tube.description.points.get_points_num() == 36
    assert sum(np.isclose(p.real[2], 0)
               for p in tube.description.points.point_to_index) == 12
    assert sum(np.isclose(p.real[2], 3)
               for p in tube.description.points.point_to_index) == 12
    assert sum(np.isclose(p.real[2], 6)
               for p in tube.description.points.point_to_index) == 12


def test_cylinder_creation_1_layer():
    cylinder = Cylinder(radius=5, height=2, r_layer_num=1, h_layer_num=1)
    assert len(cylinder.description.faces) == 24
    assert cylinder.description.points.get_points_num() == 14
    assert sum(np.isclose(p.real[2], 0)
               for p in cylinder.description.points.point_to_index) == 7
    assert sum(np.isclose(p.real[2], 2)
               for p in cylinder.description.points.point_to_index) == 7


def test_cylinder_creation_2_layer():
    cylinder = Cylinder(radius=5, height=6, r_layer_num=2, h_layer_num=2)
    assert len(cylinder.description.faces) == 96
    assert cylinder.description.points.get_points_num() == 50
    assert sum(np.isclose(p.real[2], 0)
               for p in cylinder.description.points.point_to_index) == 19
    assert sum(np.isclose(p.real[2], 3)
               for p in cylinder.description.points.point_to_index) == 12
    assert sum(np.isclose(p.real[2], 6)
               for p in cylinder.description.points.point_to_index) == 19


def test_cone_creation_1_layer():
    cone = Cone(radius=5, height=2, r_layer_num=1)
    assert len(cone.description.faces) == 12
    assert cone.description.points.get_points_num() == 8
    assert sum(np.isclose(p.real[2], 2)
               for p in cone.description.points.point_to_index) == 1
    assert sum(np.isclose(p.real[2], 0)
               for p in cone.description.points.point_to_index) == 7


def test_cone_creation_3_layer():
    cone = Cone(radius=5, height=2, r_layer_num=3)
    assert len(cone.description.faces) == 72
    assert cone.description.points.get_points_num() == 38
    assert sum(np.isclose(p.real[2], 2)
               for p in cone.description.points.point_to_index) == 1
    assert sum(np.isclose(p.real[2], 0)
               for p in cone.description.points.point_to_index) == 37
