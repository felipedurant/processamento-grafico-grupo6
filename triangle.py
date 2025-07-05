from typing import Optional
from object import Object
from material import Material
from point import Point
from vector import Vector
from ray import Ray

class Triangle(Object):
    """
    Representa um único triângulo no espaço 3D.
    Este é um objeto primitivo que pode ser renderizado.
    """
    def __init__(self, v0: Point, v1: Point, v2: Point, material: Material):
        super().__init__(material)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        # Pré-calcula as arestas e a normal para otimização
        self.edge1 = self.v1 - self.v0
        self.edge2 = self.v2 - self.v0
        self.normal = self.edge1.cross_product(self.edge2).normalize()

    def intersects(self, ray: Ray) -> Optional[float]:
        """
        Interseção raio-triângulo usando o algoritmo rápido Möller-Trumbore.
        Retorna a distância 't' ou None.
        """
        h = ray.direction.cross_product(self.edge2)
        a = self.edge1.dot_product(h)

        # Se 'a' for perto de zero, o raio é paralelo ao plano do triângulo.
        if abs(a) < 1e-6:
            return None

        f = 1.0 / a
        s = ray.origin - self.v0
        u = f * s.dot_product(h)

        if u < 0.0 or u > 1.0:
            return None

        q = s.cross_product(self.edge1)
        v = f * ray.direction.dot_product(q)

        if v < 0.0 or u + v > 1.0:
            return None

        # Neste ponto, temos uma interseção. Calculamos 't'.
        t = f * self.edge2.dot_product(q)

        if t > self.shadow_bias: # 'shadow_bias' herdado de Object
            return t
        else:
            return None

    def get_normal_at(self, point: Point) -> Vector:
        """Para sombreamento 'flat', a normal é a mesma em todo o triângulo."""
        return self.normal