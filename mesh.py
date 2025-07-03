from vector import Vector
from point import Point
from object import Object
from ray import Ray
import math

class Material:
    """
    Representa as propriedades fisicas de um material para renderizacao.

    Atributos:
        color (tuple): Cor do material como uma tupla (R, G, B).
        specular (float): Coeficiente especular do material, que afeta o brilho especular.
        lambert (float): Coeficiente lambertiano do material, que afeta a difusao da luz.
        ambient (float): Coeficiente ambiental, que afeta a luminosidade ambiente percebida.
        material_type (str): Tipo do material (por exemplo, "DIFFUSE").
        kr (float): indice de refracao do material.
        kt (float): Componente transmissiva do material, que afeta a transparencia.
    """

    def __init__(self, color, specular=0.5, lambert=1, ambient=0.2, material_type="DIFFUSE", kr=1.5, kt=0.5):
        self.color = color
        self.specular = specular 
        self.lambert = lambert  
        self.ambient = ambient  
        self.material_type = material_type 
        self.kr = kr  
        self.kt = kt  


### Classe "Mesh"
 ## - Propósito: Representa uma coleção de vértices, arestas e faces que define a forma de um objeto 3D.
  ##- Funções Comuns: Manipulação e renderização de malhas, transformações geométricas.
  
class Mesh(Object):
    """
    Representa uma malha 3D composta por vértices e triângulos.
    """

    def __init__(self, filename, material):
        self.material = material
        self.vertices = []
        self.triangles = []
        self.triangle_normals = []
        self.vertex_normals = []
        self.load_obj(filename)
        self.compute_normals()

    def load_obj(self, filename):
        """
        Lê um arquivo .OBJ simples contendo vértices e faces triangulares.
        """
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    _, x, y, z = line.strip().split()
                    self.vertices.append(Point(float(x), float(y), float(z)))
                elif line.startswith('f '):
                    _, *face = line.strip().split()
                    indices = [int(f.split('/')[0]) - 1 for f in face]
                    if len(indices) == 3:
                        self.triangles.append(tuple(indices))

    def compute_normals(self):
        """
        Calcula normais dos triângulos e médias nos vértices.
        """
        self.vertex_normals = [Vector(0, 0, 0) for _ in self.vertices]
        count = [0] * len(self.vertices)

        for tri in self.triangles:
            i1, i2, i3 = tri
            v0, v1, v2 = self.vertices[i1], self.vertices[i2], self.vertices[i3]
            normal = (v1 - v0).cross_product(v2 - v0).normalize()
            self.triangle_normals.append(normal)
            for i in tri:
                self.vertex_normals[i] += normal
                count[i] += 1

        for i in range(len(self.vertex_normals)):
            if count[i] > 0:
                self.vertex_normals[i] = (self.vertex_normals[i] / count[i]).normalize()

    def intersects(self, ray: Ray):
        """
        Testa interseção do raio com os triângulos da malha usando Möller-Trumbore.
        """
        closest_t = float('inf')
        hit_point = None

        for idx, (i1, i2, i3) in enumerate(self.triangles):
            v0, v1, v2 = self.vertices[i1], self.vertices[i2], self.vertices[i3]

            edge1 = v1 - v0
            edge2 = v2 - v0
            h = ray.direction.cross_product(edge2)
            a = edge1.dot_product(h)

            if -1e-5 < a < 1e-5:
                continue

            f = 1.0 / a
            s = ray.origin - v0
            u = f * s.dot_product(h)
            if u < 0.0 or u > 1.0:
                continue

            q = s.cross_product(edge1)
            v = f * ray.direction.dot_product(q)
            if v < 0.0 or u + v > 1.0:
                continue

            t = f * edge2.dot_product(q)
            if 1e-5 < t < closest_t:
                closest_t = t
                hit_point = ray.origin + ray.direction * t

        return hit_point  # retorna apenas o ponto
    
    def get_color(self):
        """
        Retorna a cor do material da malha.
        """
        return self.material.color
    
