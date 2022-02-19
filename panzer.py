import numpy as np
from primitives import Angle
from object_collection import Cylinder, Cone, Box, Sphere, Tube, World


def create_tube_wheel(width, radius):
    radial_layer_num = 3
    wheel = World()
    tube = Tube(radius=radius, height=width,
                r_layer_num=radial_layer_num, h_layer_num=1)
    tube.move(z=-width/2)
    tube.accept_transformations()
    tube.rotate(y=Angle(np.pi/2))
    tube.accept_transformations()
    wheel.add_object(tube)
    cone = Cone(radius=radius, height=width/8, layer_num=radial_layer_num)
    cone.rotate(y=Angle(np.pi/2))
    cone.move(x=width/2)
    cone.accept_transformations()
    wheel.add_object(cone)
    cone.rotate(z=Angle(np.pi))
    cone.accept_transformations()
    wheel.add_object(cone)
    return wheel


def main():
    world = World()
    wheel_radius = 3
    wheel_width = 30
    wheel = create_tube_wheel(wheel_width, wheel_radius)
    world.add_object(wheel)
    wheel.move(y=2*wheel_radius)
    wheel.accept_transformations()
    world.add_object(wheel)
    wheel.move(y=-4*wheel_radius)
    wheel.accept_transformations()
    world.add_object(wheel)
    small_wheel_radius = wheel_radius/2
    small_wheel = create_tube_wheel(wheel_width, small_wheel_radius)
    small_wheel.move(y=np.sqrt(2)*wheel_radius + 2*wheel_radius,
                     z=small_wheel_radius)
    small_wheel.accept_transformations()
    world.add_object(small_wheel)
    small_wheel.rotate(z=Angle(np.pi))
    small_wheel.accept_transformations()
    world.add_object(small_wheel)
    box_height = wheel_radius/2
    box = Box(width=wheel_width, height=box_height, depth=9*wheel_radius)
    box.move(z=box_height/2 + wheel_radius)
    box.accept_transformations()
    world.add_object(box)
    box_above = Box(width=0.7*wheel_width, height=box_height, depth=4*wheel_radius)
    box_above.move(z=3*box_height/2 + wheel_radius)
    box_above.accept_transformations()
    tube = Tube(radius=box_height/4, height=3*wheel_radius, r_layer_num=2,
                h_layer_num=1)
    tube.rotate(x=Angle(np.pi/2))
    tube.move(y=-2*wheel_radius, z=wheel_radius + 1.5*box_height)
    tube.accept_transformations()
    world.add_object(tube)
    world.add_object(box_above)
    world.plot()


if __name__ == "__main__":
    main()
