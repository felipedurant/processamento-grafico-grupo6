from math import sqrt, fabs
from vector import Vector

class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
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
    
    def __eq__(self, other):
        """Verifica se o ponto é igual a outro ponto."""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False

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
        
        #cria vetores que representam os lados do triangulo e a posicao relativa do ponto p em relacao ao vertice p0
        v0 = p1 - p0  #vetor do ponto p0 ao ponto p1
        v1 = p2 - p0  #vetor do ponto p0 ao ponto p2
        v2 = p - p0   #vetor do ponto p0 ao ponto p

        #calcula os produtos escalares dos vetores, que ajudam a entender como os vetores estao orientados
        d00 = v0.dot_product(v0)  #produto escalar de v0 com ele mesmo (magnitude ao quadrado de v0)
        d01 = v0.dot_product(v1)  #produto escalar de v0 com v1
        d11 = v1.dot_product(v1)  #produto escalar de v1 com ele mesmo (magnitude ao quadrado de v1)
        d20 = v2.dot_product(v0)  #produto escalar de v2 com v0
        d21 = v2.dot_product(v1)  #produto escalar de v2 com v1

        #calcula o denominador da fórmula das coordenadas baricentricas
        denom = d00 * d11 - d01 * d01

        # Caso denom seja = 0
        if (denom == 0):
            return None # Retorna None para indicar que as coordenadas não podem ser calculadas
        
        #calcula as coordenadas baricentricas v e w
        v = (d11 * d20 - d01 * d21) / denom  # Coordenada baricentrica para p1
        w = (d00 * d21 - d01 * d20) / denom  # Coordenada baricentrica para p2
        
        #calcula a coordenada baricentrica u para p0
        u = 1.0 - v - w  #a soma de u, v, e w deve ser 1

        #retorna as coordenadas baricentricas como uma tupla (u, v, w)
        return (u, v, w)

    def closest_point(self, points : list):
        """
        Recebe uma lista de pontos retornado o mais proximo.

        Args:
        points (list): Lista de pontos que serao avaliados.

        Returns:
        Point: Ponto mais proximo.
        """

        # 1. Filtra a lista para garantir que só têm objetos Point válidos
        valid_points = [p for p in points if isinstance(p, Point)]

        # 2. Se a lista de pontos válidos estiver vazia, não há o que fazer
        if not valid_points:
            return None
        
        # 3. Assume que o primeiro ponto é o mais próximo para começar
        closest = valid_points[0]
        closest_distance = self.distance_to(closest)

        # 4. Percorre o RESTANTE da lista (a partir do segundo item)
        for p in valid_points[1:]:
            distance = self.distance_to(p)
            
            # Agora a comparação é sempre entre dois números, sem risco de 'None'
            if distance < closest_distance:
                closest = p
                closest_distance = distance
            
        return closest


### Classe "Point"
##  - Propósito: Representa um ponto no espaço 3D.
##  - Funções Comuns: Armazenamento de coordenadas, operações básicas de ponto.
