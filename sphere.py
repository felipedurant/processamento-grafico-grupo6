# sphere.py
from point import Point
from vector import Vector
from color_map import Material # Precisamos do Material para as propriedades da esfera
import math

class Sphere:
    """
    Representa uma esfera em um espaço tridimensional.

    Atributos:
        center (Point): O ponto central da esfera.
        radius (float): O raio da esfera.
        material (Material): As propriedades de material da esfera (cor, brilho, etc.).
    """
    def __init__(self, center: Point, radius: float, material: Material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersect(self, ray_origin: Point, ray_direction: Vector):
        """
        Calcula a interseção entre um raio e a esfera.

        Um raio é definido por P(t) = ray_origin + t * ray_direction.
        A equação de uma esfera é (x - cx)^2 + (y - cy)^2 + (z - cz)^2 = r^2,
        que pode ser reescrita como ||P - C||^2 = r^2, onde C é o centro da esfera.

        Substituindo P(t) na equação da esfera, obtemos uma equação quadrática para t:
        ||(ray_origin + t * ray_direction) - C||^2 = r^2
        Expandindo, temos:
        (ray_direction . ray_direction)t^2 + 2 * (ray_direction . (ray_origin - C))t + ((ray_origin - C) . (ray_origin - C)) - r^2 = 0

        Onde:
        A = ray_direction . ray_direction (ou seja, ||ray_direction||^2)
        B = 2 * (ray_direction . (ray_origin - C))
        C_quad = ((ray_origin - C) . (ray_origin - C)) - r^2 (onde C_quad é o 'C' da equação quadrática Ax^2+Bx+C=0)

        Calculamos o discriminante (delta = B^2 - 4AC_quad) para encontrar as raízes 't'.
        Se delta < 0: Não há interseção.
        Se delta == 0: Há uma única interseção (o raio tangencia a esfera).
        Se delta > 0: Há duas interseções.

        Retorna:
            float or None: A menor distância 't' positiva de interseção se houver, caso contrário None.
        """
        # Vetor do centro da câmera até o centro da esfera
        # O nome do vetor aqui é 'oc' de 'origin to center'
        oc = ray_origin - self.center

        # Coeficientes da equação quadrática A*t^2 + B*t + C_quad = 0
        # A = ray_direction . ray_direction (ou seja, comprimento_squared)
        a = ray_direction.dot(ray_direction)

        # B = 2 * (ray_direction . oc)
        b = 2.0 * ray_direction.dot(oc)

        # C_quad = (oc . oc) - radius^2
        c_quad = oc.dot(oc) - self.radius**2

        # Calculando o discriminante
        discriminant = b**2 - 4*a*c_quad


        if discriminant < 0:
            # Não há interseção
            return None
        else:
            # Há uma ou duas interseções
            sqrt_discriminant = math.sqrt(discriminant)

            # Calcula as duas possíveis raízes para 't'
            t1 = (-b - sqrt_discriminant) / (2.0 * a)
            t2 = (-b + sqrt_discriminant) / (2.0 * a)

            # Queremos o 't' mais próximo e que esteja na frente da câmera (t > 0)
            if t1 > 0.001: # Usamos um pequeno epsilon para evitar auto-interseção numérica
                return t1
            elif t2 > 0.001:
                return t2
            # Se ambos os t's são negativos ou muito pequenos, a interseção está atrás do raio ou é trivial.
            return None