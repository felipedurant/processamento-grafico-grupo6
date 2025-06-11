import math
class Vector:
    """
    Representa um vetor em um espaço tridimensional.

    Atributos:
        x (float): Componente do vetor na direção X.
        y (float): Componente do vetor na direção Y.
        z (float): Componente do vetor na direção Z.
    """
    def __init__(self, x: float, y: float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    # Implemente os métodos de vetores aqui
    def length(self):
        """Calcula a magnitude (comprimento) do vetor."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        """Normaliza o vetor (torna seu comprimento 1)."""
        len_val = self.length()
        if len_val == 0:
            return Vector(0, 0, 0) # Vetor nulo se o comprimento for zero
        return Vector(self.x / len_val, self.y / len_val, self.z / len_val)

    def dot(self, other):
        """Calcula o produto escalar com outro vetor."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """Calcula o produto vetorial com outro vetor."""
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __mul__(self, scalar):
        """Multiplicação por um escalar."""
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        """Multiplicação por um escalar (permite scalar * vector)."""
        return self.__mul__(scalar)

    def __neg__(self):
        """Negação do vetor."""
        return Vector(-self.x, -self.y, -self.z)

    def __add__(self, other):
        """Adição de dois vetores."""
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    