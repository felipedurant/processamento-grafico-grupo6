import abc
from typing import Optional
from point import Point
from vector import Vector
from material import Material
from ray import Ray
from matrix import Matrix4

class Object(abc.ABC):
    """
    Classe base para todos os objetos renderizáveis da cena.
    Todo objeto possui um material que define sua aparência.
    """
    def __init__(self, material: 'Material', transform: Optional[Matrix4] = None):
        # 1. Objeto recebe um Material ao ser criado
        self.material = material
        self.transform = transform if transform is not None else Matrix4.identity()
        self.inverse_transform = self.transform.inverse() # Pré-calcula a inversa
        self.inverse_transform_transpose = self.inverse_transform.transpose()

        # Este parâmetro pode ser usado para evitar auto-interseção
        # É um valor pequeno para afastar o início de novos raios da superfície.
        self.shadow_bias = 1e-4
    
    @abc.abstractmethod
    def intersects(self, ray: Ray) -> float | None:
        """
        Verifica se o raio intersecta este objeto.
        Se sim, deve retornar a distância 't' da interseção.
        Se não, deve retornar None.
        """
        pass

    @abc.abstractmethod
    def get_normal_at(self, point: Point) -> Vector:
        """
        Método abstrato para obter a normal. As classes filhas DEVEM implementar isso.
        """
        pass


### Classe "Object"
 # - Propósito: Uma classe genérica para representar objetos 3D na cena.
 # - Funções Comuns: Armazenamento de atributos comuns a objetos 3D, como posição, rotação, escala.