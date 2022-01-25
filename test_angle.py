import numpy as np
from angle import Angle


def test_creation():
    assert Angle(0).value == 0
    assert Angle(1).value == 1
    assert Angle(3).value == 3
    assert Angle(2*np.pi).value == 0
    assert Angle(3*np.pi).value == np.pi
    assert Angle(-1).value == 2*np.pi - 1
    assert Angle(-3).value == 2*np.pi - 3
    assert Angle(-2*np.pi).value == 0
    assert Angle(-3*np.pi).value == np.pi


def test_convert():
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


def test_linspace():
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
