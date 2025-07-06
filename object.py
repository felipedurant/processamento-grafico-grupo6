import abc
from vector import Vector
from point import Point
from matrix import Matrix

class Object(abc.ABC):
    def __init__(self):
        self.parameter_min = 0.0
    
    @abc.abstractmethod
    def intersects(self, ray):
        """
        Calcula a intersecao do raio com o plano.

        Args:
            ray (Ray): O raio que pode ou nao intersectar o objeto.
        """
        pass

    @abc.abstractmethod
    def get_color(self):
        """Retorna a cor do objeto."""
        pass
    
    @abc.abstractmethod
    def get_center(self):
        """Retorna o centro do objeto."""
        pass
    
    @abc.abstractmethod
    def move(self, movement_vector : Vector):
        """Faz transformações de translação no objeto, fazendo ele se mover."""
        pass

    @abc.abstractmethod
    def rotate(self, degree : float, axis : int):
        """Faz transformações de rotação no objeto, fazendo ele girar em seu proprio eixo."""
        pass
    
    @abc.abstractmethod
    def scale(self):
        """Faz transformações de escala no objeto, fazendo ele mudar de tamanho."""
        pass

### Classe "Object"
 ## - Propósito: Uma classe genérica para representar objetos 3D na cena, possivelmente incluindo propriedades comuns a todos os objetos.
 ## - Funções Comuns: Armazenamento de atributos comuns a objetos 3D, como posição, rotação, escala.