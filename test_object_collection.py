import numpy as np
from object_collection import Plane, CircleSegment, Circle, Tube, Cylinder, Cone, ConeNoBase, Box, Sphere, World
from primitives import Angle, Point


def test_plane_creation():
    pl = Plane(width=2, height=4)
    assert len(pl.description.faces) == 2
    assert len(pl.description.points) == 4
    assert sum(np.isclose(p.real.x, -1) for p in pl.description.points) == 2
    assert sum(np.isclose(p.real.x, 1) for p in pl.description.points) == 2
    assert sum(np.isclose(p.real.y, 2) for p in pl.description.points) == 2
    assert sum(np.isclose(p.real.y, -2) for p in pl.description.points) == 2
    assert sum(np.isclose(p.real.z, 0) for p in pl.description.points) == 4


def test_segment_creation_1_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/3),
                        radius=5, layer_num=1)
    assert len(seg.description.faces) == 1
    assert (0, 1, 2) in seg.description.faces
    assert len(seg.description.points) == 3
    assert Point(0, 0, 0) in seg.description.points
    assert sum(np.isclose(p.spherical.r, 5) for p in seg.description.points) == 2


def test_segment_creation_2_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/3),
                        radius=4, layer_num=2)
    assert len(seg.description.faces) == 4
    assert len(seg.description.points) == 6
    assert Point(0, 0, 0) in seg.description.points
    assert sum(np.isclose(p.spherical.r, 2) for p in seg.description.points) == 2
    assert sum(np.isclose(p.spherical.r, 4) for p in seg.description.points) == 3


def test_segment_creation_3_layer():
    seg = CircleSegment(phi_from=Angle(0), phi_to=Angle(np.pi/2),
                        radius=9, layer_num=3)
    assert len(seg.description.faces) == 9
    assert len(seg.description.points) == 10
    assert Point(0, 0, 0) in seg.description.points
    assert sum(np.isclose(p.spherical.r, 3) for p in seg.description.points) == 2
    assert sum(np.isclose(p.spherical.r, 6) for p in seg.description.points) == 3
    assert sum(np.isclose(p.spherical.r, 9) for p in seg.description.points) == 4


def test_create_circle_1_layer():
    circle = Circle(radius=5, layer_num=1)
    assert len(circle.description.faces) == 6
    assert len(circle.description.points) == 7
    assert Point(0, 0, 0) in circle.description.points
    assert sum(np.isclose(p.spherical.r, 5) for p in circle.description.points) == 6


def test_create_circle_3_layer():
    circle = Circle(radius=9, layer_num=3)
    assert len(circle.description.faces) == 54
    assert len(circle.description.points) == 37
    assert Point(0, 0, 0) in circle.description.points
    assert sum(np.isclose(p.spherical.r, 3) for p in circle.description.points) == 6
    assert sum(np.isclose(p.spherical.r, 6) for p in circle.description.points) == 12
    assert sum(np.isclose(p.spherical.r, 9) for p in circle.description.points) == 18


def test_tube_creation_1_layer():
    tube = Tube(radius=15, height=5, r_layer_num=1, h_layer_num=1)
    assert len(tube.description.points) == 12
    assert len(tube.description.faces) == 12
    assert sum(np.isclose(p.real.z, 0) for p in tube.description.points) == 6
    assert sum(np.isclose(p.real.z, 5) for p in tube.description.points) == 6
    assert sum(np.isclose(p.spherical.r, 15) for p in tube.description.points) == 6
    assert sum(np.isclose(p.spherical.r, np.sqrt(250)) for p in tube.description.points) == 6


def test_tube_creation_3_layer():
    tube = Tube(radius=5, height=9, h_layer_num=3, r_layer_num=1)
    assert len(tube.description.faces) == 36
    assert len(tube.description.points) == 24
    assert sum(np.isclose(p.real.z, 0) for p in tube.description.points) == 6
    assert sum(np.isclose(p.real.z, 3) for p in tube.description.points) == 6
    assert sum(np.isclose(p.real.z, 6) for p in tube.description.points) == 6
    assert sum(np.isclose(p.real.z, 9) for p in tube.description.points) == 6
    assert sum(np.isclose(p.spherical.r, 5) for p in tube.description.points) == 6
    assert sum(np.isclose(p.spherical.r, np.sqrt(34)) for p in tube.description.points) == 6
    assert sum(np.isclose(p.spherical.r, np.sqrt(61)) for p in tube.description.points) == 6
    assert sum(np.isclose(p.spherical.r, np.sqrt(106)) for p in tube.description.points) == 6


def test_tube_creation_2_layer():
    tube = Tube(radius=5, height=6, h_layer_num=2, r_layer_num=2)
    assert len(tube.description.faces) == 48
    assert len(tube.description.points) == 36
    assert sum(np.isclose(p.real.z, 0) for p in tube.description.points) == 12
    assert sum(np.isclose(p.real.z, 3) for p in tube.description.points) == 12
    assert sum(np.isclose(p.real.z, 6) for p in tube.description.points) == 12
    assert sum(np.isclose(p.spherical.r, 5) for p in tube.description.points) == 12
    assert sum(np.isclose(p.spherical.r, np.sqrt(34)) for p in tube.description.points) == 12
    assert sum(np.isclose(p.spherical.r, np.sqrt(61)) for p in tube.description.points) == 12


def test_cylinder_creation_1_layer():
    c = Cylinder(radius=5, height=2, r_layer_num=1, h_layer_num=1)
    assert len(c.description.faces) == 24
    assert len(c.description.points) == 14
    assert sum(np.isclose(p.real.z, 0) for p in c.description.points) == 7
    assert sum(np.isclose(p.real.z, 2) for p in c.description.points) == 7
    assert Point(0, 0, 0) in c.description.points
    assert sum(np.isclose(p.spherical.r, 5) for p in c.description.points) == 6
    assert Point(0, 0, 2) in c.description.points
    assert sum(np.isclose(p.spherical.r, np.sqrt(29)) for p in c.description.points) == 6


def test_cylinder_creation_2_layer():
    c = Cylinder(radius=4, height=6, r_layer_num=2, h_layer_num=2)
    assert len(c.description.faces) == 96
    assert len(c.description.points) == 50
    assert sum(np.isclose(p.real.z, 0) for p in c.description.points) == 19
    assert sum(np.isclose(p.real.z, 3) for p in c.description.points) == 12
    assert sum(np.isclose(p.real.z, 6) for p in c.description.points) == 19
    assert Point(0, 0, 0) in c.description.points
    assert sum(np.isclose(p.spherical.r, 2) for p in c.description.points) == 6
    assert sum(np.isclose(p.spherical.r, 4) for p in c.description.points) == 12
    assert sum(np.isclose(p.spherical.r, 5) for p in c.description.points) == 12
    assert Point(0, 0, 6) in c.description.points
    assert sum(np.isclose(p.spherical.r, np.sqrt(40)) for p in c.description.points) == 6
    assert sum(np.isclose(p.spherical.r, np.sqrt(52)) for p in c.description.points) == 12


def test_cone_creation_1_layer():
    cone = Cone(radius=5, height=2, layer_num=1)
    assert len(cone.description.faces) == 12
    assert len(cone.description.points) == 8
    assert sum(np.isclose(p.real.z, 0) for p in cone.description.points) == 7
    assert Point(0, 0, 0) in cone.description.points
    assert Point(0, 0, 2) in cone.description.points
    assert sum(np.isclose(p.spherical.r, 5) for p in cone.description.points) == 6


def test_cone_creation_3_layer():
    cone = Cone(radius=9, height=18, layer_num=3)
    assert len(cone.description.faces) == 108
    assert len(cone.description.points) == 56
    assert sum(np.isclose(p.real.z, 0) for p in cone.description.points) == 37
    assert Point(0, 0, 0) in cone.description.points
    assert Point(0, 0, 18) in cone.description.points
    assert sum(np.isclose(p.spherical.r, 3) for p in cone.description.points) == 6
    assert sum(np.isclose(p.spherical.r, 6) for p in cone.description.points) == 12
    assert sum(np.isclose(p.spherical.r, 9) for p in cone.description.points) == 18
    assert sum(np.isclose(p.real.z, 6) for p in cone.description.points) == 12
    assert sum(np.isclose(p.real.z, 12) for p in cone.description.points) == 6


def test_cone_no_base_creation_1_layer():
    cone = ConeNoBase(radius=5, height=2, layer_num=1)
    assert len(cone.description.faces) == 6
    assert len(cone.description.points) == 7
    assert sum(np.isclose(p.real.z, 0) for p in cone.description.points) == 6
    assert Point(0, 0, 2) in cone.description.points
    assert sum(np.isclose(p.spherical.r, 5) for p in cone.description.points) == 6


def test_cone_no_base_creation_3_layer():
    cone = ConeNoBase(radius=9, height=18, layer_num=3)
    assert len(cone.description.faces) == 54
    assert len(cone.description.points) == 37
    assert sum(np.isclose(p.real.z, 0) for p in cone.description.points) == 18
    assert Point(0, 0, 18) in cone.description.points
    assert sum(np.isclose(p.spherical.r, 9) for p in cone.description.points) == 18
    assert sum(np.isclose(p.real.z, 6) for p in cone.description.points) == 12
    assert sum(np.isclose(p.real.z, 12) for p in cone.description.points) == 6



def test_box_creation():
    box = Box(width=2, height=4, depth=6)
    assert len(box.description.faces) == 12
    assert len(box.description.points) == 8
    assert sum(np.isclose(p.real.x, -1) for p in box.description.points) == 4
    assert sum(np.isclose(p.real.x, 1) for p in box.description.points) == 4
    assert sum(np.isclose(p.real.y, -3) for p in box.description.points) == 4
    assert sum(np.isclose(p.real.y, 3) for p in box.description.points) == 4
    assert sum(np.isclose(p.real.z, -2) for p in box.description.points) == 4
    assert sum(np.isclose(p.real.z, 2) for p in box.description.points) == 4


def test_sphere_creation_split_1():
    sph = Sphere(radius=5, split_num=1)
    assert len(sph.description.faces) == 8
    assert len(sph.description.points) == 6
    assert sum(np.isclose(p.spherical.r, 5) for p in sph.description.points) == 6


def test_sphere_creation_split_2():
    sph = Sphere(radius=7, split_num=2)
    assert len(sph.description.faces) == 32
    assert len(sph.description.points) == 18
    assert sum(np.isclose(p.spherical.r, 7) for p in sph.description.points) == 18


def test_sphere_creation_split_3():
    sph = Sphere(radius=7, split_num=3)
    assert len(sph.description.faces) == 128
    assert len(sph.description.points) == 66
    assert sum(np.isclose(p.spherical.r, 7) for p in sph.description.points) == 66


def test_world_add_object():
    pl1 = Plane(width=3, height=5)
    pl1.rotate(x=Angle(np.pi/2))
    pl1.move(y=10)
    pl1.accept_transformations()
    pl1.rotate(x=Angle(np.pi/2))
    pl2 = Plane(width=10, height=8)
    world = World()
    world.add_object(pl1)
    world.add_object(pl2)
    assert len(world.description.faces) == 4
    assert len(world.description.points) == 8
    assert sum(np.isclose(p.real.z, 0) for p in world.description.points) == 4
    assert sum(np.isclose(p.real.z, 10) for p in world.description.points) == 4
    assert sum(np.isclose(p.real.z, 2.5) for p in pl1.description.points) == 2
    assert sum(np.isclose(p.real.z, -2.5) for p in pl1.description.points) == 2
    assert all(x == 0 for x in pl1.description.moves.values())
    assert pl1.description.rotations['x'] == Angle(np.pi/2)
    assert pl1.description.rotations['y'] == Angle(0)
    assert pl1.description.rotations['z'] == Angle(0)
