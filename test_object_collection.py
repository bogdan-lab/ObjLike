import numpy as np
from collection_2d import CircleSegment
from primitives import Angle


def test_segment_creation_1_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/3),
                        radius=5, layer_num=1)
    assert len(seg.description.faces) == 1
    assert (0, 1, 2) in seg.description.faces
    assert seg.description.points.get_points_num() == 3
    out_l = seg.outer_layer_points
    assert len(out_l) == 2
    assert all([np.isclose(p.spherical[0], seg.radius) for p in out_l])
    assert all([out_l[i].spherical[1] < out_l[i+1].spherical[1]
                for i in range(len(out_l)-1)])


def test_segment_creation_2_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/3),
                        radius=4, layer_num=2)
    assert len(seg.description.faces) == 4
    assert seg.description.points.get_points_num() == 6
    out_l = seg.outer_layer_points
    assert len(out_l) == 3
    assert all([np.isclose(p.spherical[0], seg.radius) for p in out_l])
    assert all([out_l[i].spherical[1] < out_l[i+1].spherical[1]
                for i in range(len(out_l)-1)])


def test_segment_creation_3_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/2),
                        radius=9, layer_num=3)
    assert len(seg.description.faces) == 9
    assert seg.description.points.get_points_num() == 10
    out_l = seg.outer_layer_points
    assert len(out_l) == 4
    assert all([np.isclose(p.spherical[0], seg.radius) for p in out_l])
    assert all([out_l[i].spherical[1] < out_l[i+1].spherical[1]
                for i in range(len(out_l)-1)])
