import numpy as np

import create_element as ce


# Cyllinder tests


def test_add_point_index_1():
    input_radius = 10
    segments = ce.create_layered_segments(input_radius, layer_num=1)
    segments = ce.normalize_angles(segments)
    polar_points, counted_segments = ce.add_point_index(segments)
    assert len(counted_segments) == 6
    assert all([el[0] == [[0, (0, 0)]] for el in counted_segments])
    assert all(len(el) == 2 for el in counted_segments)
    assert all(len(el[1]) == 2 for el in counted_segments)
    assert len(polar_points) == 7


def test_connect_polar_points_1():
    segments = ce.create_layered_segments(radius=10, layer_num=1)
    segments = ce.normalize_angles(segments)
    polar_points, counted_segments = ce.add_point_index(segments)
    faces = ce.connect_polar_points(counted_segments)
    origin = polar_points.index((0, 0))
    assert all([origin in el for el in faces])
    assert len(faces) == 6
    assert all(len(el) == 3 for el in faces)
    assert np.max(faces) == 6


def test_connect_polar_points_2():
    segments = ce.create_layered_segments(radius=10, layer_num=2)
    segments = ce.normalize_angles(segments)
    polar_points, counted_segments = ce.add_point_index(segments)
    faces = ce.connect_polar_points(counted_segments)
    assert len(polar_points) == 19
    assert len(faces) == 24
    assert all(len(el) == 3 for el in faces)
    assert np.max(faces) == 18


def test_connect_polar_points_3():
    segments = ce.create_layered_segments(radius=10, layer_num=3)
    segments = ce.normalize_angles(segments)
    polar_points, counted_segments = ce.add_point_index(segments)
    faces = ce.connect_polar_points(counted_segments)
    assert len(polar_points) == 37
    assert len(faces) == 54
    assert all(len(el) == 3 for el in faces)
    assert np.max(faces) == 36


def test_move_object_1():
    input_points = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
    dist = 2
    dir_vec = (1, 0, 0)
    points = ce.move(input_points, dir_vec, dist)
    expected = [(2, 0, 0), (3, 1, 1), (4, 2, 2)]
    assert all(all(np.isclose(lhs, rhs))
               for lhs, rhs in zip(points, expected))


def test_move_object_2():
    input_points = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
    dist = 3
    dir_vec = (0, 1, 0)
    points = ce.move(input_points, dir_vec, dist)
    expected = [(0, 3, 0), (1, 4, 1), (2, 5, 2)]
    assert all(all(np.isclose(lhs, rhs))
               for lhs, rhs in zip(points, expected))


def test_move_object_3():
    input_points = [(0, 0, 0), (1, 1, 1), (2, 2, 2)]
    dist = 3
    dir_vec = (4, 0, 3)
    points = ce.move(input_points, dir_vec, dist)
    expected = [(2.4, 0, 1.8), (3.4, 1, 2.8), (4.4, 2, 3.8)]
    assert all(all(np.isclose(lhs, rhs))
               for lhs, rhs in zip(points, expected))


def test_merge_1():
    p1, f1 = [(0, 0, 0), (2, 2, 2), (3, 3, 3)], [(0, 1, 2)]
    p2, f2 = [(10, 10, 10), (12, 12, 12), (13, 13, 13)], [(0, 1, 2)]
    points, faces = ce.merge([(p1, f1), (p2, f2)])
    assert points == [(0, 0, 0), (2, 2, 2), (3, 3, 3),
                      (10, 10, 10), (12, 12, 12), (13, 13, 13)]
    assert faces == [(0, 1, 2), (3, 4, 5)]


def test_merge_2():
    p1, f1 = [(0, 0, 0), (2, 2, 2), (3, 3, 3)], [(0, 1, 2)]
    p2, f2 = [(10, 10, 10), (12, 12, 12), (3, 3, 3)], [(0, 1, 2)]
    points, faces = ce.merge([(p1, f1), (p2, f2)])
    assert points == [(0, 0, 0), (2, 2, 2), (3, 3, 3),
                      (10, 10, 10), (12, 12, 12)]
    assert faces == [(0, 1, 2), (3, 4, 2)]
