from typing import List
from point import Point
from material import Material
from triangle import Triangle

class Mesh:
    """
    Uma classe que lê dados de uma malha (vértices e faces)
    e os converte em uma lista de objetos 'Triangle' renderizáveis.
    """
    def __init__(self, vertices: List[Point], faces: List[tuple], material: Material):
        """
        Args:
            vertices (List[Point]): A lista de todos os pontos da malha.
            faces (List[tuple]): Lista de tuplas, onde cada tupla contém 3 índices
                                 que apontam para os vértices de um triângulo.
                                 Ex: (0, 1, 2)
            material (Material): O material a ser aplicado a todos os triângulos da malha.
        """
        self.vertices = vertices
        self.faces = faces
        self.material = material
        self.triangles = self._build_triangles()

    def _build_triangles(self) -> List[Triangle]:
        """
        Cria a lista de objetos Triangle a partir dos vértices e faces.
        """
        triangle_list = []
        for face in self.faces:
            # Pega os 3 vértices que formam o triângulo usando os índices da face
            v0 = self.vertices[face[0]]
            v1 = self.vertices[face[1]]
            v2 = self.vertices[face[2]]
            
            # Cria o objeto Triangle e o adiciona à lista
            triangle_list.append(Triangle(v0, v1, v2, self.material))
            
        return triangle_list