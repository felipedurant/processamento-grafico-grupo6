from vector import Vector
class Point:
    """
    Representa um ponto em um espaço tridimensional.

    Atributos:
        x (float): Coordenada X do ponto.
        y (float): Coordenada Y do ponto.
        z (float): Coordenada Z do ponto.
    """

    def __init__(self, x: float, y: float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    # Implemente os métodos de pontos aqui
    def __sub__(self, other):
        """
        Subtração de dois pontos (resulta em um vetor)
        ou subtração de um vetor de um ponto (resulta em um ponto).
        """
        if isinstance(other, Point):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, Vector): # <-- ADIÇÃO AQUI
            return Point(self.x - other.x, self.y - other.y, self.z - other.z) # <-- ADIÇÃO AQUI
        raise TypeError(f"Operação de subtração não suportada entre Point e {type(other)}.")

    def __add__(self, other):
        """Adição de um ponto e um vetor (resulta em um ponto)."""
        if isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        raise TypeError("Apenas vetores podem ser adicionados a um ponto.")

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"