import numpy as np
from primitives import Point, PointCollection, FaceCollection, Angle, RealCoordinates, SphericalCoordinates


def test_convert_spher_point_to_real():
    assert all(np.isclose(
            Point.convert_spherical_point_to_real(
                    SphericalCoordinates(5, Angle(np.pi/2), Angle(np.pi))),
                    RealCoordinates(0, 0, -5)))
    assert all(np.isclose(
            Point.convert_spherical_point_to_real(
                    SphericalCoordinates(5, Angle(np.pi/2), Angle(np.pi/2))),
                    RealCoordinates(0, 5, 0)))
    assert all(np.isclose(
            Point.convert_spherical_point_to_real(
                    SphericalCoordinates(5, Angle(0), Angle(np.pi/2))),
                    RealCoordinates(5, 0, 0)))
    assert all(np.isclose(
                 Point.convert_spherical_point_to_real(
                         SphericalCoordinates(0, Angle(0), Angle(0))),
                         RealCoordinates(0, 0, 0)))


def test_convert_real_to_spher():
    sph_point = Point.convert_real_point_to_spherical(RealCoordinates(0, 0, 0))
    assert np.isclose(sph_point.r, 0)
    assert np.isclose(sph_point.phi.value, 0)
    assert np.isclose(sph_point.theta.value, 0)
    sph_point = Point.convert_real_point_to_spherical(RealCoordinates(3, 0, 0))
    assert np.isclose(sph_point.r, 3)
    assert np.isclose(sph_point.phi.value, 0)
    assert np.isclose(sph_point.theta.value, np.pi/2)
    sph_point = Point.convert_real_point_to_spherical(RealCoordinates(0, 3, 0))
    assert np.isclose(sph_point.r, 3)
    assert np.isclose(sph_point.phi.value, np.pi/2)
    assert np.isclose(sph_point.theta.value, np.pi/2)
    sph_point = Point.convert_real_point_to_spherical(RealCoordinates(0, 0, 3))
    assert np.isclose(sph_point.r, 3)
    assert np.isclose(sph_point.phi.value, 0)
    assert np.isclose(sph_point.theta.value, 0)


def test_convert_both_ways():
    sph_point = SphericalCoordinates(1, Angle(2), Angle(3))
    res_sph = Point.convert_real_point_to_spherical(
                    Point.convert_spherical_point_to_real(sph_point))
    assert np.isclose(res_sph.r, sph_point.r)
    assert np.isclose(res_sph.phi.value, sph_point.phi.value)
    assert np.isclose(res_sph.theta.value, sph_point.theta.value)
    real_point = RealCoordinates(1, 2, 3)
    res_real = Point.convert_spherical_point_to_real(
                    Point.convert_real_point_to_spherical(real_point))
    assert all(np.isclose(real_point, res_real))


def test_create_from_spherical():
    point = Point.from_spherical(5, Angle(np.pi/2), Angle(np.pi))
    assert all(np.isclose(point.real, (0, 0, -5)))
    point2 = Point.from_spherical(5, Angle(np.pi/2), Angle(np.pi/2))
    assert all(np.isclose(point2.real, (0, 5, 0)))


def test_move_point():
    point = Point(1, 2, 3)
    assert point.move(3, 2, 1, inplace=False) == Point(4, 4, 4)
    assert point.move(x=3,) == Point(4, 2, 3)
    assert point == Point(1, 2, 3)
    assert point.move(1, 1, 1, inplace=True) == Point(2, 3, 4)
    assert point == Point(2, 3, 4)


def test_point_rotate_x():
    point = Point(1, 0, 0)
    assert all([Point(1, 0, 0) == point.rotate_x(Angle(alpha))
               for alpha in np.linspace(0, 5*np.pi, 100)])
    point = Point(0, 1, 0)
    point.rotate_x(Angle(np.pi/2), inplace=True)
    expected = Point(0, 0, 1)
    assert all(np.isclose(point.real, expected.real))
    point = Point(0, 1, 0)
    point.rotate_x(Angle(-np.pi/2), inplace=True)
    expected = Point(0, 0, -1)
    assert all(np.isclose(point.real, expected.real))
    point = Point(0, 1, 0)
    res = point.rotate_x(Angle(np.pi/4), inplace=False)
    expected = Point(0, np.sqrt(2)/2, np.sqrt(2)/2)
    assert point == Point(0, 1, 0)
    assert all(np.isclose(res.real, expected.real))


def test_point_rotate_y():
    point = Point(0, 1, 0)
    assert all([Point(0, 1, 0) == point.rotate_y(Angle(alpha))
               for alpha in np.linspace(0, 5*np.pi, 100)])
    point = Point(1, 0, 0)
    point.rotate_y(Angle(np.pi/2), inplace=True)
    expected = Point(0, 0, -1)
    assert all(np.isclose(point.real, expected.real))
    point = Point(1, 0, 0)
    point.rotate_y(Angle(-np.pi/2), inplace=True)
    expected = Point(0, 0, 1)
    assert all(np.isclose(point.real, expected.real))
    point = Point(0, 0, 1)
    res = point.rotate_y(Angle(np.pi/4), inplace=False)
    expected = Point(np.sqrt(2)/2, 0, np.sqrt(2)/2)
    assert point == Point(0, 0, 1)
    assert all(np.isclose(res.real, expected.real))


def test_point_rotate_z():
    point = Point(0, 0, 1)
    assert all([Point(0, 0, 1) == point.rotate_z(Angle(alpha))
               for alpha in np.linspace(0, 5*np.pi, 100)])
    point = Point(0, 1, 0)
    point.rotate_z(Angle(np.pi/2), inplace=True)
    expected = Point(-1, 0, 0)
    assert all(np.isclose(point.real, expected.real))
    point = Point(0, 1, 0)
    point.rotate_z(Angle(-np.pi/2), inplace=True)
    expected = Point(1, 0, 0)
    assert all(np.isclose(point.real, expected.real))
    point = Point(0, 1, 0)
    res = point.rotate_z(Angle(np.pi/4), inplace=False)
    expected = Point(-np.sqrt(2)/2, np.sqrt(2)/2, 0)
    assert point == Point(0, 1, 0)
    assert all(np.isclose(res.real, expected.real))


def test_collection_adding_points():
    collection = PointCollection()
    assert collection.add_point(Point(0, 0, 0)) == 0
    assert collection.add_point(Point(0, 0, 1)) == 1
    assert collection.add_point(Point(0, 1, 1)) == 2
    assert collection.add_point(Point(1, 1, 1)) == 3
    assert collection.add_point(Point(0, 0, 0)) == 0
    assert collection.add_point(Point(1, 1, 1)) == 3


def test_get_str_content():
    collection = PointCollection()
    collection.add_point(Point(0, 0, 0))
    collection.add_point(Point(1, 0, 0))
    collection.add_point(Point(1, 2, 0))
    collection.add_point(Point(1, 2, 3))
    data = collection.get_file_str_content()
    assert len(data) == 4
    assert data[0].strip() == 'p 0 0 0'
    assert data[1].strip() == 'p 1 0 0'
    assert data[2].strip() == 'p 1 2 0'
    assert data[3].strip() == 'p 1 2 3'


def test_move_point_collection_not_inplace():
    collection = PointCollection()
    collection.add_point(Point(0, 0, 0))
    collection.add_point(Point(1, 0, 0))
    collection.add_point(Point(1, 2, 0))
    initial = collection
    res = collection.move(1, 2, 3, inplace=False)
    expected = PointCollection()
    expected.add_point(Point(1, 2, 3))
    expected.add_point(Point(2, 2, 3))
    expected.add_point(Point(2, 4, 3))
    assert res == expected
    assert collection == initial


def test_move_point_collection_inplace():
    collection = PointCollection()
    collection.add_point(Point(0, 0, 0))
    collection.add_point(Point(1, 0, 0))
    collection.add_point(Point(1, 2, 0))
    res = collection.move(1, 2, 3, inplace=True)
    expected = PointCollection()
    expected.add_point(Point(1, 2, 3))
    expected.add_point(Point(2, 2, 3))
    expected.add_point(Point(2, 4, 3))
    assert res == expected
    assert collection == res


def test_get_point():
    collection = PointCollection()
    collection.add_point(Point(0, 0, 0))
    collection.add_point(Point(1, 0, 0))
    collection.add_point(Point(1, 2, 0))
    collection.add_point(Point(1, 2, 3))
    assert len(collection) == 4
    assert collection.get_point(0) == Point(0, 0, 0)
    assert collection.get_point(1) == Point(1, 0, 0)
    assert collection.get_point(2) == Point(1, 2, 0)
    assert collection.get_point(3) == Point(1, 2, 3)


def test_face_collection_add_face():
    test = FaceCollection()
    test.add_face(Point(1, 0, 0), Point(0, 1, 0), Point(0, 0, 1))
    assert len(test.faces) == 1
    assert len(test.points) == 3
    assert (0, 1, 2) in test.faces
    test.add_face(Point(1, 0, 0), Point(0, 1, 0), Point(0, 1, 1))
    assert len(test.faces) == 2
    assert len(test.points) == 4
    assert (0, 1, 3) in test.faces
    test.add_face(Point(1, 0, 0), Point(0, 1, 0), Point(0, 0, 1))
    assert len(test.faces) == 2


def test_face_collection_accept_transformation_move_only():
    test = FaceCollection()
    test.add_face(Point(1, 0, 0), Point(0, 1, 0), Point(0, 0, 1))
    test.move(x=1, y=2, z=3)
    assert test.moves == {'x': 1, 'y': 2, 'z': 3}
    test.move(x=5)
    assert test.moves == {'x': 6, 'y': 2, 'z': 3}
    assert test.points.point_to_index == {Point(1, 0, 0): 0,
                                          Point(0, 1, 0): 1,
                                          Point(0, 0, 1): 2}
    test.accept_transformations()
    assert test.moves == {'x': 0, 'y': 0, 'z': 0}
    assert test.points.point_to_index == {Point(7, 2, 3): 0,
                                          Point(6, 3, 3): 1,
                                          Point(6, 2, 4): 2}


def test_face_collection_accept_transformation_rotate_only():
    test = FaceCollection()
    test.add_face(Point(1, 0, 0), Point(0, 1, 0), Point(0, 0, 1))
    test.rotate(x=Angle(np.pi/2), y=Angle(np.pi/2), z=Angle(np.pi/2))
    assert test.rotations == {'x': Angle(np.pi/2), 'y': Angle(np.pi/2),
                              'z': Angle(np.pi/2)}
    test.rotate(x=Angle(np.pi/2))
    assert test.rotations == {'x': Angle(np.pi), 'y': Angle(np.pi/2),
                              'z': Angle(np.pi/2)}
    assert test.points.point_to_index == {Point(1, 0, 0): 0,
                                          Point(0, 1, 0): 1,
                                          Point(0, 0, 1): 2}
    test.accept_transformations()
    assert test.rotations == {'x': Angle(0), 'y': Angle(0), 'z': Angle(0)}
    real_points = [p.real for p in test.points]
    assert len(real_points) == 3
    assert all(np.isclose(real_points[0], (0, 0, -1)))
    assert all(np.isclose(real_points[1], (1, 0, 0)))
    assert all(np.isclose(real_points[2], (0, -1, 0)))


def test_face_collection_save_to_file(tmp_path):
    test = FaceCollection()
    test.add_face(Point(1, 0, 0), Point(0, 1, 0), Point(0, 0, 1))
    test.add_face(Point(1, 0, 0), Point(0, 1, 0), Point(0, 1, 1))
    test.move(x=1, y=2, z=3)
    filename = tmp_path / "test.obj_like"
    test.save_to_file(filename)
    with open(filename, 'r') as fin:
        data = fin.read().split('\n')
    assert len(data) == 10
    assert list(map(float, data[0].split()[1:])) == [1, 0, 0]
    assert list(map(float, data[1].split()[1:])) == [0, 1, 0]
    assert list(map(float, data[2].split()[1:])) == [0, 0, 1]
    assert list(map(float, data[3].split()[1:])) == [0, 1, 1]
    assert all(['sp' in line for line in data[:4]])
    assert list(map(float, data[4].split()[1:])) == [2, 2, 3]
    assert list(map(float, data[5].split()[1:])) == [1, 3, 3]
    assert list(map(float, data[6].split()[1:])) == [1, 2, 4]
    assert list(map(float, data[7].split()[1:])) == [1, 3, 4]
    assert all(['wp' in line for line in data[4:8]])
    assert list(map(int, data[8].split()[1:])) == [0, 1, 2]
    assert list(map(int, data[9].split()[1:])) == [0, 1, 3]
    assert all(['s ' in line for line in data[8:]])


def test_merge_collections():
    lhs = FaceCollection()
    lhs.add_face(Point(1, 0, 0), Point(0, 1, 0), Point(0, 0, 1))
    rhs = FaceCollection()
    rhs.add_face(Point(1, 0, 0), Point(0, 1, 0), Point(0, 1, 1))
    res = FaceCollection.merge(lhs, rhs)
    assert len(res.faces) == 2
    assert len(res.points) == 4
    assert Point(1, 0, 0) in res.points.point_to_index
    assert Point(0, 1, 0) in res.points.point_to_index
    assert Point(0, 0, 1) in res.points.point_to_index
    assert Point(0, 1, 1) in res.points.point_to_index


def test_angle_creation():
    assert Angle(0).value == 0
    assert Angle(1).value == 1
    assert Angle(3).value == 3
    assert Angle(2*np.pi).value == 0
    assert Angle(3*np.pi).value == np.pi
    assert Angle(-1).value == 2*np.pi - 1
    assert Angle(-3).value == 2*np.pi - 3
    assert Angle(-2*np.pi).value == 0
    assert Angle(-3*np.pi).value == np.pi


def test_angle_convert():
    values = np.linspace(0, np.pi, 6, endpoint=True)
    res = Angle.convert(values)
    assert all([r.value == v for r, v in zip(res, values)])
    values = np.linspace(0, 2*np.pi, 3, endpoint=True)
    res = Angle.convert(values)
    assert values[0] == res[0].value
    assert values[1] == res[1].value
    assert 0 == res[2].value
    values = np.linspace(-2*np.pi, -np.pi, 6, endpoint=True)
    res = Angle.convert(values)
    exp = np.linspace(0, np.pi, 6, endpoint=True)
    assert all([r.value == v for r, v in zip(res, exp)])


def test_angle_linspace():
    values = np.linspace(0, np.pi, 6, endpoint=True)
    res = Angle.linspace(Angle(0), Angle(np.pi), 6, endpoint=True)
    assert all([r.value == v for r, v in zip(res, values)])
    values = np.linspace(0, np.pi, 6, endpoint=False)
    res = Angle.linspace(Angle(0), Angle(np.pi), 6, endpoint=False)
    assert all([r.value == v for r, v in zip(res, values)])
    values = np.linspace(0, 2*np.pi, 4, endpoint=True)
    res = Angle.linspace(Angle(0), Angle(2*np.pi), 4, endpoint=True)
    assert res[0].value == values[0]
    assert res[1].value == values[1]
    assert res[2].value == values[2]
    assert res[3].value == values[0]
    res = Angle.linspace(Angle(-2*np.pi), Angle(0), 4, endpoint=True)
    assert res[0].value == values[0]
    assert res[1].value == values[1]
    assert res[2].value == values[2]
    assert res[3].value == values[0]
