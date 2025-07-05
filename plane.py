from point import Point
from vector import Vector
from object import Object
from material import Material
from ray import Ray
from typing import Optional

class Plane(Object):
    """
    Representa um plano geometrico infinito.
    """
    def __init__(self, point: Point, normal: Vector, material: Material, one_side=True):
        """
        Inicializa o Plano

        Args:
            point (Point): Um ponto no plano.
            normal (Vector): O vetor normal ao plano.
            material (Material): O material que define a aparência do plano.
            one_side (bool): Se True, o plano só é visível pelo lado para onde a normal aponta.
        """
        super().__init__(material)
        self.point = point
        self.normal = normal.normalize()
        self.one_side = one_side

    def __repr__(self) -> str:
        """
        Fornece uma representacao em string da instancia de Plane.
        """
        return f"Plane(point={self.point}, normal={self.normal})"

    def intersects(self, ray: Ray) -> float | None:
        """
        Calcula a intersecao do raio com o plano.

        Returns:
            A distância 't' da interseção, ou None se não houver interseção.
        """

        # Denominador da fórmula de interseção raio-plano
        denom = ray.direction.dot_product(self.normal)

        # Se one_side for True, só consideramos colisões frontais (raio contra a normal)
        if self.one_side and denom >= 0:
            return None

        # Evita divisão por zero (raio paralelo ao plano)
        # Usamos um valor pequeno (epsilon) para segurança com floats
        if abs(denom) > 1e-6:
            # Numerador da fórmula de interseção
            numer = (self.point - ray.origin).dot_product(self.normal)
            t = numer / denom
            
            # Garante que a interseção esteja à frente do raio
            if t > self.shadow_bias: # 'shadow_bias' herdado de Object
                return t
        
        return None


    # Para um plano, a normal é constante, mas para outras formas, ela depende do ponto de interseção.
    def get_normal_at(self, point: Optional[Point] = None) -> Vector:
        """
        Retorna o vetor normal na superfície do objeto em um ponto específico.
        Para um plano, a normal é constante em toda a sua superfície.
        """
        return self.normal
    


### Classe "Plane"
##  - Propósito: Representa um plano infinito ou limitado em 3D.
##  - Funções Comuns: Definição de plano por ponto e normal, cálculos de interseção com raios.
