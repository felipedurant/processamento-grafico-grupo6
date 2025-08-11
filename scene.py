from typing import List, Union
from point import Point
from vector import Vector
from object import Object
from mesh import Mesh
import random
import math

class Light:
    """Representa uma fonte de luz pontual com posição e intensidade."""
    def __init__(self, position: Point, intensity: tuple = (255, 255, 255)):
        self.position = position
        self.intensity = intensity

class RectangularLight:
    """
    Representa uma fonte de luz retangular que emite raios paralelos.
    Funciona como uma janela ou um painel de luz.
    """
    def __init__(self, position: Point, direction: Vector, u_vec: Vector, v_vec: Vector, intensity: tuple):
        """
        Args:
            position (Point): O centro do retângulo.
            direction (Vector): A direção para a qual a luz é emitida (deve ser normalizada).
            u_vec (Vector): Vetor que representa a 'largura' do retângulo.
            v_vec (Vector): Vetor que representa a 'altura' do retângulo.
            intensity (tuple): A cor e intensidade da luz (R, G, B).
        """
        self.position = position
        self.direction = direction.normalize()
        self.u_vec = u_vec  # Vetor da largura
        self.v_vec = v_vec  # Vetor da altura
        self.intensity = intensity

    def get_random_point(self) -> Point:
        """Retorna um ponto aleatório na superfície do retângulo."""
        # Gera dois números aleatórios entre -0.5 e 0.5
        rand_u = random.random() - 0.5
        rand_v = random.random() - 0.5
        # Desloca o ponto central ao longo dos vetores da largura e altura
        return self.position + (self.u_vec * rand_u) + (self.v_vec * rand_v)

# Um tipo que pode ser qualquer uma das fontes de luz
LightSource = Union[Light, RectangularLight]

class Scene:
    """
    Representa o mundo a ser renderizado.
    Contém a lista de todos os objetos e fontes de luz.
    """
    def __init__(self, ambient_light: tuple = (255, 255, 255)):
        self.objects: List[Object] = []
        self.lights: List[LightSource] = []
        self.ambient_light = ambient_light

    def add(self, obj: Object):
        """Adiciona um único objeto (como Sphere ou Plane) à cena."""
        self.objects.append(obj)

    def add_mesh(self, mesh: Mesh):
        """
        Adiciona todos os triângulos de um objeto Mesh à cena.
        É um método de conveniência para não ter que fazer isso no main.
        """
        self.objects.extend(mesh.triangles)

    def add_light(self, light: LightSource):
        """Adiciona uma fonte de luz (representada por sua posição) à cena."""
        self.lights.append(light)