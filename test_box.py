from box import Box
from primitives import Point, Angle
import pytest
import numpy as np


@pytest.fixture(name="cube")
def fixture_cube() -> Box:
    origin = Point(0, 0, 0)
    return Box(origin, 1, 1, 1)


def test_move_box_not_inplace(cube):
    initial = cube
    res = cube.move(1, 2, 3, inplace=False)
    assert initial == cube
    expected = Box(cube.origin.move(1, 2, 3, inplace=False),
                   cube.width, cube.height, cube.depth)
    assert res == expected


def test_move_box_inplace(cube):
    expected = Box(cube.origin.move(1, 2, 3, inplace=False),
                   cube.width, cube.height, cube.depth)
    res = cube.move(1, 2, 3, inplace=True)
    assert res == expected
    assert res == cube


def test_save_to_file(tmp_path, cube):
    filename = tmp_path / "cube.obj_like"
    cube.save_to_file(filename)
    with open(filename, 'r') as fin:
        data = fin.read().split('\n')
    assert len(data) == 20
    assert "p 0 0 0" in data[:8]
    assert "p 1 0 0" in data[:8]
    assert "p 0 1 0" in data[:8]
    assert "p 1 1 0" in data[:8]
    assert "p 0 0 1" in data[:8]
    assert "p 0 1 1" in data[:8]
    assert "p 1 0 1" in data[:8]
    assert "p 1 1 1" in data[:8]
    assert "s 0 1 2" in data[8:]
    assert "s 1 3 2" in data[8:]
    assert "s 4 5 6" in data[8:]
    assert "s 7 6 5" in data[8:]
    assert "s 5 4 2" in data[8:]
    assert "s 0 2 4" in data[8:]
    assert "s 7 1 6" in data[8:]
    assert "s 7 3 1" in data[8:]
    assert "s 7 5 3" in data[8:]
    assert "s 5 2 3" in data[8:]
    assert "s 1 4 6" in data[8:]
    assert "s 1 0 4" in data[8:]


def test_rotate_around_z_180(cube):
    initial_pts = cube.points.point_to_index
    cube.rotate_z(Angle(np.pi))
    res_pts = cube.points.point_to_index
    for (ip, rp) in zip(initial_pts, res_pts):
        assert all(np.isclose(rp.real, (-ip.real[0], -ip.real[1], ip.real[2])))


def test_rotate_around_z_90(cube):
    initial_pts = cube.points.point_to_index
    cube.rotate_z(Angle(-np.pi/2))
    res_pts = cube.points.point_to_index
    for (ip, rp) in zip(initial_pts, res_pts):
        assert all(np.isclose(rp.real, (ip.real[1], -ip.real[0], ip.real[2])))


def test_rotate_around_y_180(cube):
    initial_pts = cube.points.point_to_index
    cube.rotate_y(Angle(np.pi))
    res_pts = cube.points.point_to_index
    for (ip, rp) in zip(initial_pts, res_pts):
        assert all(np.isclose(rp.real, (-ip.real[0], ip.real[1], -ip.real[2])))


def test_rotate_around_y_90(cube):
    initial_pts = cube.points.point_to_index
    cube.rotate_y(Angle(-np.pi/2))
    res_pts = cube.points.point_to_index
    for (ip, rp) in zip(initial_pts, res_pts):
        assert all(np.isclose(rp.real, (-ip.real[2], ip.real[1], ip.real[0])))


def test_rotate_around_x_180(cube):
    initial_pts = cube.points.point_to_index
    cube.rotate_x(Angle(np.pi))
    res_pts = cube.points.point_to_index
    for (ip, rp) in zip(initial_pts, res_pts):
        assert all(np.isclose(rp.real, (ip.real[0], -ip.real[1], -ip.real[2])))


def test_rotate_around_x_90(cube):
    initial_pts = cube.points.point_to_index
    cube.rotate_x(Angle(-np.pi/2))
    res_pts = cube.points.point_to_index
    for (ip, rp) in zip(initial_pts, res_pts):
        assert all(np.isclose(rp.real, (ip.real[0], ip.real[2], -ip.real[1])))
