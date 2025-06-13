from math import sqrt, fabs
from vector import Vector

class Point:
    def __init__(self, x=0, y=0, z=0):
        """ Inicializa um ponto com coordenadas x, y, e z. """
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """ Representacao em string do ponto. """
        return f"Point({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        """ Adiciona as coordenadas de outro ponto ou vetor a este ponto. """
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """ Subtrai as coordenadas de outro ponto ou vetor deste ponto, retornando um vetor. """
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance_to(self, other):
        """ Calcula a distancia euclidiana ate outro ponto. """
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def midpoint(self, other):
        """ Calcula o ponto medio entre este ponto e outro ponto. """
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2, (self.z + other.z) / 2)

    def move_towards(self, other, fraction=0.5):
        """ Move este ponto em direcao a outro ponto por uma fracao da distancia. """
        return Point(self.x + (other.x - self.x) * fraction,
                     self.y + (other.y - self.y) * fraction,
                     self.z + (other.z - self.z) * fraction)

    @staticmethod
    def barycentric_coords(p, p0, p1, p2):
        """ Calcula as coordenadas baricentricas de um ponto p em relacao ao triangulo formado por p0, p1, e p2. """
        v0 = Vector(p1.x - p0.x, p1.y - p0.y, p1.z - p0.z)
        v1 = Vector(p2.x - p0.x, p2.y - p0.y, p2.z - p0.z)
        v2 = Vector(p.x - p0.x, p.y - p0.y, p.z - p0.z)
        
        d00 = v0.dot_product(v0)
        d01 = v0.dot_product(v1)
        d11 = v1.dot_product(v1)
        d20 = v2.dot_product(v0)
        d21 = v2.dot_product(v1)
        
        denom = d00 * d11 - d01 * d01
        v = (d11 * d20 - d01 * d21) / denom
        w = (d00 * d21 - d01 * d20) / denom
        u = 1.0 - v - w
        
        return u, v, w

    def closest_point(self, points : list):
        """
        Recebe uma lista de pontos retornado o mais proximo.

        Args:
        points (list): Lista de pontos que serao avaliados.

        Returns:
        Point: Ponto mais proximo.
        """
        if len(points) > 0:
            closest = None
            closest_distance = None
            for p in points:
                if isinstance(p, Point):
                    if closest == None:
                        closest = p
                        closest_distance = self.distance_to(p)
                    else:
                        distance = self.distance_to(p)
                        if closest_distance > distance:
                            closest = p
                            closest_distance = distance
        return closest


### Classe "Point"
##  - Propósito: Representa um ponto no espaço 3D.
##  - Funções Comuns: Armazenamento de coordenadas, operações básicas de ponto.
