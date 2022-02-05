from collection_2d import Circle
from primitives import Point, PointCollection
from typing import List, Tuple


class Cylinder:

    def _build_cylinder(self) -> None:
        bot = Circle(self.origin, self.radius, self.layer_num)
        top = Circle(self.origin, self.radius, self.layer_num)
        moved_points = PointCollection()
        for p in top.points.point_to_index:
            moved_points.add_point(
                    Point(p.real[0], p.real[1], p.real[2] + self.height))
        top.points = moved_points
        moved_outer = []
        for p in top.outer_layer_points:
            moved_outer.append(Point(p.real[0], p.real[1],
                                     p.real[2] + self.height))
        top.outer_layer_points = moved_outer
        side_points = list(zip(bot.outer_layer_points, top.outer_layer_points))
        self.points = PointCollection()
        self.faces = []
        for i in range(len(side_points)-1):
            self.faces.append(
                    (self.points.add_point(side_points[i][1]),
                     self.points.add_point(side_points[i+1][0]),
                     self.points.add_point(side_points[i][0])))
            self.faces.append(
                    (self.points.add_point(side_points[i+1][0]),
                     self.points.add_point(side_points[i+1][1]),
                     self.points.add_point(side_points[i][1])))
        self.faces.append(
                    (self.points.add_point(side_points[-1][0]),
                     self.points.add_point(side_points[0][0]),
                     self.points.add_point(side_points[-1][1])))
        self.faces.append(
                    (self.points.add_point(side_points[0][0]),
                     self.points.add_point(side_points[0][1]),
                     self.points.add_point(side_points[-1][1])))
        for f in bot.faces:
            self.faces.append(
                    (self.points.add_point(bot.points.get_point(f[0])),
                     self.points.add_point(bot.points.get_point(f[1])),
                     self.points.add_point(bot.points.get_point(f[2]))))
        for f in top.faces:
            self.faces.append(
                    (self.points.add_point(top.points.get_point(f[0])),
                     self.points.add_point(top.points.get_point(f[1])),
                     self.points.add_point(top.points.get_point(f[2]))))

    def __init__(self, origin: Point, radius: float, height: float,
                 layer_num: int) -> None:
        self.origin = origin
        self.radius = radius
        self.height = height
        self.layer_num = layer_num
        self._build_cylinder()

    def get_real_points_as_tuples(self) -> List[Tuple[float, float, float]]:
        '''Retruns correctly ordered sequence of the points as tuples with
        real coordinates in it'''
        return [p.real for p in self.points.point_to_index]
