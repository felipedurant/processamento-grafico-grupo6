from ray import *
from vector import *
from point import *
from object import *

class Sphere(Object):
    def __init__(self, center : Point, radius : float, color : tuple):
        super().__init__()
        self.center : Point = center
        self.radius : float = radius
        self.color : tuple = color

    def intersects(self, ray : Ray):
        ray_direction = ray.get_direction()
        oc : Vector = ray.get_origin() - self.center
        a = ray_direction.dot_product(ray_direction)
        b = 2.0 * oc.dot_product(ray_direction)
        c = oc.dot_product(oc) - self.radius * self.radius
        delta = b * b - 4 * a * c
        if delta > 0:
            # Raio intersecta a esfera
            if delta > 0:
                t1 = (-b + sqrt(delta))/(2 * a)
                t2 = (-b - sqrt(delta))/(2 * a)
                points = []
                if t1 > self.parameter_min:
                    points.append(ray.get_point_by_parameter(t1))
                if t2 > self.parameter_min:
                    points.append(ray.get_point_by_parameter(t2))
                if len(points) > 0:
                    return ray.get_origin().closest_point(points)
            else:
                t = (-b)/(2 * a)
                if t > self.parameter_min:
                    return ray.get_point_by_parameter(t)
        # Raio não intersecta a esfera
        return None
    
    def get_color(self):
        return self.color


##Classe "Sphere"
 ## - Propósito: Representa uma esfera em 3D.
 ## - Funções Comuns: Definição de centro e raio, cálculos de interseção com raios.
