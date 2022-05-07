from os import mkdir
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from primitives import Angle
from object_collection import Cylinder, Box, Sphere, Cone, World


def create_tube_wheel(width, radius):
    wheel = Cylinder(radius=radius, height=width, r_layer_num=3, h_layer_num=3)
    wheel.move(z=-width/2)
    wheel.accept_transformations()
    wheel.rotate(y=Angle(np.pi/2))
    wheel.accept_transformations()
    return wheel


def main():
    folder = Path("./simple_scene")
    if not folder.exists():
        mkdir(folder)

    world = World()

    cylinder = Cylinder(radius=10, height=30, r_layer_num=3, h_layer_num=1)
    cylinder.rotate(y=Angle(np.pi/2))
    cylinder.accept_transformations()
    cylinder.rotate(z=Angle(-np.pi/6))
    cylinder.move(z=10, x=-15, y=-10)
    cylinder.accept_transformations()
    cylinder.save_to_file(folder/"cyllinder.json")
    world.add_object(cylinder)

    cone = Cone(radius=10, height=20, layer_num=3)
    cone.rotate(x=Angle(np.pi))
    cone.move(z=20, y=20)
    cone.accept_transformations()
    cone.save_to_file(folder/"cone.json")
    world.add_object(cone)

    sph = Sphere(radius=10, split_num=3)
    sph.move(y=20, z=30)
    sph.accept_transformations()
    sph.save_to_file(folder/"sphere.json")
    world.add_object(sph)

    box_lamp = Box(width=25, height=35, depth=2)
    box_lamp.move(z=30, y=-48)
    box_lamp.accept_transformations()
    box_lamp.save_to_file(folder/"box_lamp.json")
    world.add_object(box_lamp)

    bounding_box = Box(width=40, height=50, depth=100)
    bounding_box.move(z=25)
    bounding_box.accept_transformations()
    bounding_box.invert()
    bounding_box.save_to_file(folder/"bounding_box.json")
    #world.add_object(bounding_box)

    world.plot()
    plt.show()


if __name__ == "__main__":
    main()
