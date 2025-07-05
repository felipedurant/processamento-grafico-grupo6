# Em um novo arquivo: scene.py

from typing import List
from point import Point
from object import Object
from mesh import Mesh # Importamos Mesh para o método 'add_mesh'

class Scene:
    """
    Representa o mundo a ser renderizado.
    Contém a lista de todos os objetos e fontes de luz.
    """
    def __init__(self):
        self.objects: List[Object] = []
        self.lights: List[Point] = []

    def add(self, obj: Object):
        """Adiciona um único objeto (como Sphere ou Plane) à cena."""
        self.objects.append(obj)

    def add_mesh(self, mesh: Mesh):
        """
        Adiciona todos os triângulos de um objeto Mesh à cena.
        É um método de conveniência para não ter que fazer isso no main.
        """
        self.objects.extend(mesh.triangles)

    def add_light(self, light_position: Point):
        """Adiciona uma fonte de luz (representada por sua posição) à cena."""
        self.lights.append(light_position)