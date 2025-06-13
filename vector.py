from math import sqrt, fabs

"""
Define uma classe chamada Vector que representa um vetor tridimensional.
A classe Vector eh projetada para realizar operacoes vetoriais comuns.
"""

class Vector:
    AIR_REFRACTIVE_INDEX = 1  # Constante de indice de refracao do ar

    def __init__(self, x=0, y=0, z=0):
        """ Inicializa um vetor com componentes x, y e z. """
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        """ Representacao em string do vetor. """
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        """ Adiciona dois vetores. """
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """ Subtrai dois vetores. """
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        """ Negacao do vetor (inverte o sinal de cada componente). """
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        """ Multiplica por um escalar ou realiza o produto escalar com outro vetor. """
        if isinstance(other, Vector):
            return self.dot_product(other)
        return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        """ Multiplicacao reversa para suportar escalar * vetor. """
        return self.__mul__(other)

    def __truediv__(self, other):
        """ Divide os componentes do vetor por um escalar. """
        return Vector(self.x / other, self.y / other, self.z / other)

    def magnitude(self):
        """ Calcula a magnitude do vetor. """
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        """ Retorna o vetor unitario. """
        magnitude = self.magnitude()
        if magnitude != 0:
            return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)
        else:
            return Vector()

    def dot_product(self, other):
        """ Retorna o produto escalar entre dois vetores. """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other):
        """ Calcula o produto vetorial com outro vetor. """
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def scale(self, factor):
        """ Escala o vetor por um fator multiplicativo. """
        return self * factor

    def invert(self):
        """ Inverte o sinal de cada componente do vetor. """
        return -self

    def reflect(self, normal):
        """ Reflete o vetor sobre um plano definido por um vetor normal. """
        normalized_normal = normal.normalize()
        return self - 2 * self.dot_product(normalized_normal) * normalized_normal

    def clamp_value(self, value, min_value, max_value):
        """ Restringe um valor entre um minimo e um maximo. """
        return max(min_value, min(max_value, value))

    def refract(self, normal, refractive_index):
        """ Calcula o vetor de refracao com base no indice de refracao fornecido. """
        cosi = self.clamp_value(self.dot_product(normal), -1, 1)
        etai_over_etat = self.AIR_REFRACTIVE_INDEX / refractive_index if cosi < 0 else refractive_index / self.AIR_REFRACTIVE_INDEX
        normal = normal if cosi < 0 else -normal
        cosi = fabs(cosi)
        k = 1 - etai_over_etat ** 2 * (1 - cosi ** 2)
        return Vector(0, 0, 0) if k < 0 else etai_over_etat * self + (etai_over_etat * cosi - sqrt(k)) * normal

    def fresnel(self, normal, refractive_index):
        """ Calcula o coeficiente de Fresnel para refracao e reflexao baseado no indice de refracao. """
        cosi = fabs(self.clamp_value(self.dot_product(normal), -1, 1))
        sint = self.AIR_REFRACTIVE_INDEX / refractive_index * sqrt(max(0, 1 - cosi ** 2))
        if sint >= 1:
            return 1
        cost = sqrt(max(0, 1 - sint ** 2))
        rs = ((refractive_index * cosi) - (self.AIR_REFRACTIVE_INDEX * cost)) / ((refractive_index * cosi) + (self.AIR_REFRACTIVE_INDEX * cost))
        rp = ((self.AIR_REFRACTIVE_INDEX * cosi) - (refractive_index * cost)) / ((self.AIR_REFRACTIVE_INDEX * cosi) + (refractive_index * cost))
        return (rs ** 2 + rp ** 2) / 2


### Classe "Vector"
##  - Propósito: Manipula vetores em 2D ou 3D.
##  - Funções Comuns: Operações vetoriais (adição, subtração, produto escalar e vetorial), normalização.
