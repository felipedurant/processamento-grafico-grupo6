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
        self.radius_scale : float = 1

    def intersects(self, ray : Ray):
        """Ferifica se há alguma intersecção entre o ray e a esfera."""
        ray_direction = ray.get_direction()
        oc : Vector = ray.get_origin() - self.center
        a = ray_direction.dot_product(ray_direction)
        b = 2.0 * oc.dot_product(ray_direction)
        c = oc.dot_product(oc) - self.get_radius() * self.get_radius()
        delta = b * b - 4 * a * c
        if delta >= 0:
            # Raio intersecta a esfera
            if delta > 0:
                t1 = (-b + sqrt(delta))/(2 * a)
                t2 = (-b - sqrt(delta))/(2 * a)
                times = []
                if t1 > self.parameter_min:
                    times.append(t1)
                if t2 > self.parameter_min:
                    times.append(t2)
                if len(times) > 0:
                    return {"t" : min(times), "color" : self.get_color()}
            else:
                t = (-b)/(2 * a)
                if t > self.parameter_min:
                    return {"t" : t, "color" : self.get_color()}
        # Raio não intersecta a esfera
        return None
    
    def get_radius(self):
        return self.radius * self.radius_scale

    def get_color(self):
        """Retorna a cor da esfera."""
        return self.color

    def get_center(self):
        """Retorna o centro da esfera."""
        return self.center
    
    def move(self, movement_vector : Vector):
        """Função que movimenta a esfera a partir de uma transformação de translação."""
        move_matrix = Matrix.create_move_matrix(movement_vector)
        self.center = move_matrix.dot_product(self.center)
    
    def rotate(self, degree : float, axis : int):
        pass
    
    def scale(self, new_scale : float):
        self.radius_scale = new_scale


##Classe "Sphere"
 ## - Propósito: Representa uma esfera em 3D.
 ## - Funções Comuns: Definição de centro e raio, cálculos de interseção com raios.
