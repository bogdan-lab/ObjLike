from os import mkdir
from pathlib import Path
import matplotlib.pyplot as plt
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

    cylinder = Cylinder(radius=10, height=30, r_layer_num=2, h_layer_num=2)
    cylinder.move(y=-30)
    cylinder.accept_transformations()
    cylinder.save_to_file(folder/"cyllinder.json")
    world.add_object(cylinder)

    cone = Cone(radius=10, height=30, layer_num=2)
    cone.save_to_file(folder/"cone.json")
    world.add_object(cone)

    sph = Sphere(radius=10, split_num=2)
    sph.move(y=30, z=10)
    sph.accept_transformations()
    sph.save_to_file(folder/"sphere.json")
    world.add_object(sph)

    box_lamp = Box(width=2, height=5, depth=40)
    box_lamp.move(z=50, x=-20)
    box_lamp.accept_transformations()
    box_lamp.save_to_file(folder/"box_lamp.json")
    world.add_object(box_lamp)

    bounding_box = Box(width=40, height=60, depth=100)
    bounding_box.move(z=30)
    bounding_box.accept_transformations()
    bounding_box.invert()
    bounding_box.save_to_file(folder/"bounding_box.json")
    world.add_object(bounding_box)

    world.plot()
    plt.show()


if __name__ == "__main__":
    main()
