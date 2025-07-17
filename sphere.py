from math import sqrt
from typing import Optional

from ray import Ray
from vector import Vector
from point import Point
from object import Object
from material import Material
from matrix import Matrix4

class Sphere(Object):
    """
    Representa uma esfera em 3D.
    """
    def __init__(self, material: Material, transform: Optional[Matrix4] = None):
        """
        Inicializa a Esfera.

        Args:
            center (Point): O ponto central da esfera.
            radius (float): O raio da esfera. Deve ser um valor positivo.
            material (Material): O material que define a aparência da esfera.
        """

        super().__init__(material, transform)

    def __repr__(self) -> str:
        """Fornece uma representação em string da instância de Sphere."""
        return f"Sphere(transform=\n{self.transform}\n)"

    def intersects(self, ray: Ray) -> Optional[float]:
        """
        Calcula a interseção do raio com a esfera usando a fórmula quadrática.
        
        Retorna:
            A distância 't' da interseção mais próxima, ou None se não houver.
        """

        local_ray = ray.transform(self.inverse_transform)

        # Vetor do centro da esfera para a origem do raio
        oc = local_ray.origin - Point(0, 0, 0)

        # Coeficientes da equação quadrática (a*t^2 + b*t + c = 0)
        # 'a' é 1 porque a direção do raio é normalizada
        a = local_ray.direction.dot_product(local_ray.direction)
        b = 2.0 * oc.dot_product(local_ray.direction)
        c = oc.dot_product(oc) - 1.0 # raio ao quadrado = 1

        delta = b**2 - 4 * a * c 

        # Se o discriminante for negativo, não há interseção real
        if delta < 0:
            return None
        
        # Calcula as duas possíveis soluções para 't'
        sqrt_d = sqrt(delta)
        t1 = (-b - sqrt_d) / (2 * a)
        t2 = (-b + sqrt_d) / (2 * a)

        # Verifica a interseção mais próxima que está à frente do raio
        if t1 > self.shadow_bias:
            return t1  # t1 é a primeira e mais próxima interseção
        if t2 > self.shadow_bias:
            return t2  # t2 é a única interseção à frente (raio começou dentro da esfera)
            
        return None
    
    def get_normal_at(self, local_point: 'Point') -> 'Vector':
        """
        Calcula o vetor normal na superfície da esfera em um ponto específico.
        """
        # A normal da esfera é o vetor do seu centro até o ponto na superfície.
        return (local_point - Point(0, 0, 0)).normalize()


##Classe "Sphere"
 ## - Propósito: Representa uma esfera em 3D.
 ## - Funções Comuns: Definição de centro e raio, cálculos de interseção com raios.
