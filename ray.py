from vector import *

class Ray(object):
    """
    Classe que representa um raio com uma origem e uma direcao.
    """
    def __init__(self, origin, direction):
        """
        Inicializa um Ray com uma origem e uma direcao normalizada.
        
        Args:
        origin (Point): O ponto de origem do raio.
        direction (Vector): O vetor direcao do raio.
        """
        self.origin = origin
        self.direction = direction.normalize()

    def get_point_by_parameter(self, t):
        """
        Retorna um ponto neste raio dado um parametro t.
        
        Args:
        t (float): O parametro que define um ponto ao longo do raio atraves da equacao parametrica.
        
        Returns:
        Vector: Ponto no raio correspondente ao parametro t.
        """
        return self.origin + self.direction.scale(t)

    def get_point_by_distance(self, dist):
        """
        Retorna um ponto neste raio a uma distancia especificada.
        
        Args:
        dist (float): A distancia ao longo do raio a partir da origem.
        
        Returns:
        Vector: Ponto no raio a uma distancia especificada.
        """
        return self.origin + self.direction * dist

    def get_inverted_ray(self):
        """
        Retorna um novo raio com a direcao invertida.
        
        Returns:
        Ray: Novo raio com direcao invertida.
        """
        return Ray(self.origin, self.direction.invert())

    def __repr__(self):
        """
        Retorna uma representacao string do objeto Ray.
        
        Returns:
        str: Representacao do Ray no formato 'Ray(origin, direction)'.
        """
        return f'Ray({repr(self.origin)}, {repr(self.direction)})'
    
    def set_direction(self, vector : Vector):
        """
        Determina o valor do vetor de direção como o valor do vetor recebido.
        
        Args:
        vector (Vector): Novo vetor de direção.
        """
        self.direction = vector
        pass

    def get_direction(self):
        """
        Returns:
        Vector: Vetor de direção do Ray.
        """
        return self.direction
    
    def change_direction(self, vector : Vector):
        """
        Muda a direção que o vetor de direção aponta, o movendo de acordo a sua soma com o vetor recebido.

        Args:
        vector (Vector): Netor que é somado ao vetor de direção. 
        """
        self.direction = self.direction + vector

    def get_origin(self):
        return self.origin


### Classe "Ray"
##  - Propósito: Representa um raio, comumente usado em algoritmos de ray tracing.
##  - Funções Comuns: Definição de origem e direção do raio, cálculos de interseção com objetos.
