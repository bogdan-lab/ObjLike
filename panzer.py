import numpy as np
import matplotlib.pyplot as plt
from primitives import Angle
from object_collection import Cylinder, Box, Sphere, Tube, World, Plane


def create_tube_wheel(width, radius):
    wheel = Cylinder(radius=radius, height=width, r_layer_num=3, h_layer_num=3)
    wheel.move(z=-width/2)
    wheel.accept_transformations()
    wheel.rotate(y=Angle(np.pi/2))
    wheel.accept_transformations()
    return wheel


def main():
    world = World()
    wheel = create_tube_wheel(width=30, radius=1)
    world.add_object(wheel)
    wheel.move(y=2*wheel.radius)
    wheel.accept_transformations()
    world.add_object(wheel)
    wheel.move(y=-4*wheel.radius)
    wheel.accept_transformations()
    world.add_object(wheel)
    wheel.move(y=-2*wheel.radius)
    wheel.accept_transformations()
    world.add_object(wheel)
    wheel.move(y=8*wheel.radius)
    wheel.accept_transformations()
    world.add_object(wheel)

    small_wheel = create_tube_wheel(wheel.height, wheel.radius/2)
    small_wheel.move(y=np.sqrt(2)*wheel.radius + 4*wheel.radius,
                     z=small_wheel.radius)
    small_wheel.accept_transformations()
    world.add_object(small_wheel)
    small_wheel.rotate(z=Angle(np.pi))
    small_wheel.accept_transformations()
    world.add_object(small_wheel)

    box = Box(width=1.15*wheel.height, height=wheel.radius,
              depth=13*wheel.radius)
    box.move(z=box.height/2 + world.get_max_z())
    box.accept_transformations()
    world.add_object(box)

    pos_plane = Plane(width=small_wheel.radius, height=box.depth)
    pos_plane.rotate(y=Angle(np.pi/2))
    pos_plane.move(x=world.get_max_x(), z=box.get_min_z() - pos_plane.width/2)
    pos_plane.accept_transformations()
    world.add_object(pos_plane)
    pos_plane.rotate(z=Angle(np.pi))
    pos_plane.accept_transformations()
    world.add_object(pos_plane)

    box_above = Box(width=0.7*wheel.height, height=0.75*wheel.radius,
                    depth=4*wheel.radius)
    box_above.move(z=box_above.height/2 + world.get_max_z())
    box_above.accept_transformations()
    world.add_object(box_above)

    tube = Tube(radius=box_above.height/4, height=8*wheel.radius,
                r_layer_num=2, h_layer_num=4)
    tube.rotate(x=Angle(np.pi/2))
    tube.move(y=-2*wheel.radius,
              z=0.5*(box_above.get_min_z() + box_above.get_max_z()))
    tube.accept_transformations()
    world.add_object(tube)

    sphere = Sphere(radius=tube.radius, split_num=3)
    sphere.move(z=0.5*(tube.get_min_z() + tube.get_max_z()),
                y=world.get_min_y() - tube.height/2)
    sphere.accept_transformations()
    world.add_object(sphere)
    world.save_to_file("test.json")
    world.plot()
    plt.show()


if __name__ == "__main__":
    main()
