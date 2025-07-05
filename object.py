import abc
from material import Material

class Object(abc.ABC):
    """
    Classe base para todos os objetos renderizáveis da cena.
    Todo objeto possui um material que define sua aparência.
    """
    def __init__(self, material: Material):
        # 1. Objeto recebe um Material ao ser criado
        self.material = material

        # Este parâmetro pode ser usado para evitar auto-interseção
        # É um valor pequeno para afastar o início de novos raios da superfície.
        self.shadow_bias = 1e-4
    
    @abc.abstractmethod
    def intersects(self, ray) -> float | None:
        """
        Verifica se o raio intersecta este objeto.
        Se sim, deve retornar a distância 't' da interseção.
        Se não, deve retornar None.
        """
        pass


### Classe "Object"
 ## - Propósito: Uma classe genérica para representar objetos 3D na cena.
 ## - Funções Comuns: Armazenamento de atributos comuns a objetos 3D, como posição, rotação, escala.