from vector import Vector
from point import Point # para o 'origin'

class Ray:
    """
    Classe que representa um raio com uma origem e uma direcao.
    A direção é SEMPRE normalizada automaticamente.
    """
    def __init__(self, origin: Point, direction: Vector):
        self.origin = origin
        # Ao atribuir a direção aqui, o método especial de 'setter' já será chamado
        self.direction = direction

    @property
    def direction(self) -> Vector:
        """Este é o 'getter'. Ele apenas retorna o valor que está guardado."""
        return self._direction

    @direction.setter
    def direction(self, new_vector: Vector):
        """
        Este é o 'setter'. Ele é chamado TODA VEZ que se faz 'ray.direction = ...'
        Aqui a lógica de normalização foi centralizada.
        """
        self._direction = new_vector.normalize()

    def point_at(self, distance: float) -> Point:
        """
        Retorna um ponto no raio a uma 'distance' específica da origem.
        (Substitui get_point_by_parameter e get_point_by_distance)
        """
        # self.direction está seguro e normalizado
        return self.origin + self.direction * distance

    def __repr__(self) -> str:
        """ Retorna uma representacao em string do objeto Ray. """
        return f'Ray({repr(self.origin)}, {repr(self.direction)})'