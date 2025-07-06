from object import *
from material import *
from point import *
from plane import *
from ray import *

class Mesh(Object):
    def __init__(self, vertices : list, triples : list, n_triangles: int, n_vertices : int,
                 color: tuple, normals_triangles = None, normals_vertices = None):
        """
        Malha que é formada por um conjunto de triangulos que juntos formam um objeto 3D.

        Args:
        vertices ([Point]): Lista de pontos que representam os vertices dos triangulos.
        triples ([(int, int, int)]): Triplas que contem 3 inteiros que são os indices dos vertices de um triangulo.
        n_triangles (int): Número de triangulos na malha.
        n_vertices (int): Número de vertices na malha.
        color: (tupla): tupla com a cor da malha (r, g, b).
        normals_triangles ([Vector]): Lista de vetores normais dos triangulos.
        normal_vertices ([Vector]): Lista de vetores normais dos vertices.

        Returns:
        Retorna a malha se for uma malha valida ou None se for uma malha invalida.
        """
        super().__init__()
        self.n_triangles : int = n_triangles
        self.n_vertices : int = n_vertices
        self.vertices : list = self.set_vertices(vertices)
        self.triples : list = self.set_triples(triples)
        if self.n_vertices >= 3 and self.n_triangles > 0 and \
            len(self.vertices) == self.n_vertices and len(self.triples) == self.n_triangles:
            self.color : tuple = color
            self.normals_triangles : list
            self.normals_vertices : list
            if normals_triangles == None or len(normals_triangles) != self.n_triangles:
                self.normals_triangles = self.create_triangles_normals_list()
            else:
                self.normals_triangles = normals_triangles
            if normals_vertices == None or len(normals_vertices) != self.n_vertices:
                self.normals_vertices = self.create_vertices_normals_list()
            else:
                self.normals_vertices = normals_vertices
        else:
            return None

    def set_vertices(self, vertices_list : list):
        """
        Define a lista de vertices.
        Se um elemento da na lista não for Point ele é removido da lista,
        e consequentimente a malha será invalida. 
        
        Args:
        vertices_list ([Point]): Lista de pontos que serão os vertices dos triangulos.

        Returns:
        [Point]: Lista de vertices que foi atribuida a malha.
        """
        vertices = [] 
        for v in vertices_list:
            if isinstance(v, Point):
                vertices.append(v)
        self.vertices = vertices
        return self.vertices
    
    def get_vertice(self, v_index):
        """
        Retorna um dos pontos da lista de vertices de acordo com o indice recebido.
        
        Args:
        v_index (int): Indice do vertice na lista de vertices.

        Returns:
        Retorna o Vertice com indice = v_index ou None se o indice for maior que o tamanho da lista ou menor que zero.
        """
        if v_index >= 0 and v_index < self.n_vertices:
            return self.vertices[v_index]
        else:
            return None

    def set_triples(self, triples_list : list):
        """
        Define a lista de triplas que representam os triangulos da malha.
        Se um elemento da lista não for uma tripla valida ele é removido da lista,
        e consequentimente a malha será invalida.
        
        Args:
        triples_list ([((int, int, int))]): Lista de triplas com 3 inteiros que são os indices dos vertices.

        Returns:
        [((int, int, int))]: Lista de triplas que foi atribuida a malha.
        """
        clean_triples_list = []
        for t in triples_list:
            if self.is_valid_triple(t):
                clean_triples_list.append(t)
        self.triples = clean_triples_list
        return triples_list
    
    def is_valid_triple(self, triple):
        """
        Determina se a tripla é valida para a malha.
        
        Args:
        triple ((int, int, int)): Tripla com 3 inteiros.

        Returns:
        Bool: retorna true se a tupla for valida e false se não for valida.
        """
        return isinstance(triple, tuple) and len(triple) == 3 and self.get_vertice(triple[0]) != None and\
            self.get_vertice(triple[1]) != None and self.get_vertice(triple[2]) != None

    def create_triangles_normals_list(self):
        """
        Cria a lista de vetores normais dos triangulos da malha.
        Para cada tripla, forma dois vetores com os vertices do triangulo,
        faz o produto cruzado entre esses vetores e normaliza o resultado (resultando em um vetor normal)
        e adiciona esse vetor normal em uma lista que será retornada.

        Returns:
        [Vector]: Lista de vetores normais dos triangulos.
        """
        normals_list = []
        for i in range(self.n_triangles):
            triple = self.triples[i]
            vec1 = self.get_vertice(triple[1]) - self.get_vertice(triple[0])
            vec2 = self.get_vertice(triple[2]) - self.get_vertice(triple[1])
            vec_normal = vec1.cross_product(vec2).normalize()
            normals_list.append(vec_normal)
        return normals_list
    
    def create_vertices_normals_list(self):
        """
        Cria a lista de vetores normais dos vertices da malha.
        Cria uma lista de vetores vazios para serem os vetores dos vertices,
        para cada tripla (triangulo), faz a soma de cada um dos vetores dos vertices com o vetor
        normal do triangulo e o resultado atualiza a lista de vetores de vertices,
        no fim os vetores dos vertices são normalizados e retornados.

        Returns:
        [Vector]: Lista de vetores normais dos vertices.
        """
        vertices_normals = [Vector()]*self.n_vertices
        for i in range(self.n_triangles):
            triple = self.triples[i]
            for index in triple:
                vertices_normals[index] +=  self.normals_triangles[i]
        for i in range(self.n_vertices):
            vertices_normals[i] = vertices_normals[i].normalize()
        return vertices_normals

    def intersects(self, ray : Ray):
        """
        Percorre todos os triangulos da malha e verifica se eles colidem com o raio,
        retornando as informações do mais proximo.
        Para cada triangulo, cria um plano que contem o triangulo e verifica se o raio colide
        com esse plano, se sim verifica se o ponto de colisão está dentro da area do triangulo,
        se estiver dentro da area do triangulo considerase que esse raio colidiu com esse triangulo
        e compara para ver se esse triangulo é o mais proximo da camera. 

        Args:
        ray (Ray): O raio da camera que pode ou nao intersectar a malha.

        Returns:
        Dicionario com informações da colisão: parametro t, cor, vetor normal do triangulo que colidiu.
        """
        lower_t = float("inf")
        lower_info = None
        # Percorre triangulos:
        for i in range(self.n_triangles):
            triangle = self.triples[i]
            triangle_normal = self.normals_triangles[i]
            # Cria plano que contem triangulo:
            triangle_plane = Plane(self.get_vertice(triangle[0]), triangle_normal, Material(0, 0, 0))
            # Verifica colisão com plano do triangulo:
            plane_collision_info = triangle_plane.intersects(ray)
            if plane_collision_info != None:
                colision_point = ray.get_point_by_parameter(plane_collision_info["t"])
                # Verifica se o ponto de colisão está dentro do triangulo:
                if self.point_in_triangle(colision_point, triangle):
                    # Verifica e atualiza o mais proximo:
                    if lower_t > plane_collision_info["t"]:
                        lower_t = plane_collision_info["t"]
                        lower_info = {"t" : plane_collision_info["t"], "color" : self.get_color(),
                                      "triangle_normal" : triangle_normal}
        return lower_info

    def point_in_triangle(self, point : Point, triangle : tuple):
        """Indica se o ponto está ou não dentro do triangulo."""
        vert1 = self.get_vertice(triangle[0])
        vert2 = self.get_vertice(triangle[1])
        vert3 = self.get_vertice(triangle[2])
        bc_cord = Point.barycentric_coords(point, vert1, vert2, vert3)
        u = bc_cord[0]
        v = bc_cord[1]
        w = bc_cord[2]
        if u >= 0 and u <= 1 and v >= 0 and v <= 1 and w >= 0 and w <= 1:
            return True
        else:
            return False
    
    def get_color(self):
        """
        Retorna a cor da malha.

        Returns:
        Retorna a tupla com 3 elementos (r, g, b) que está associada a cor da malha.
        """
        return self.color
    
    def get_center(self):
        """Retorna o centro da mesh, fazendo a soma de todos os seus pontos para tirar a media eles."""
        total_point = Point()
        for p in self.vertices:
            total_point += p
        center_x = total_point.x / self.n_vertices
        center_y = total_point.y / self.n_vertices
        center_z = total_point.z / self.n_vertices
        center_point = Point(center_x, center_y, center_z) 
        return center_point
    
    def apply_transform(self, transformation_matrix : Matrix):
        """
        Função responsavel por aplicar a transformação para todos os pontos da mesh e atualizar os vetores normais.
        """
        for i in range(self.n_vertices):
            self.vertices[i] = transformation_matrix.dot_product(self.vertices[i])
        self.normals_triangles = self.create_triangles_normals_list()
        self.normals_vertices = self.create_vertices_normals_list()
    
    def move(self, movement_vector : Vector):
        """Função que movimenta a mesh a partir de uma transformação de translação."""
        move_matrix = Matrix.create_move_matrix(movement_vector)
        self.apply_transform(move_matrix)
    
    def rotate(self, degree : float, axis : int):
        """Função que rotaciona a mesh a partir de uma transformação de rotação."""
        move_vector = Point() - self.get_center()
        position_to_center = Matrix.create_move_matrix(move_vector)
        rotation_matrix = Matrix.create_rotation_matrix(degree, axis)
        center_to_position = position_to_center.inverse()
        t = center_to_position.dot_product(rotation_matrix).dot_product(position_to_center)
        self.apply_transform(t)
    
    def scale(self, scale_vector : Vector):
        """Função que muda a escala da mesh a partir de uma transformação de escala."""
        move_vector = Point() - self.get_center()
        position_to_center = Matrix.create_move_matrix(move_vector)
        scale_matrix = Matrix.create_scale_matrix(scale_vector)
        center_to_position = position_to_center.inverse()
        t = center_to_position.dot_product(scale_matrix).dot_product(position_to_center)
        self.apply_transform(t)
        pass

### Classe "Mesh"
 ## - Propósito: Representa uma coleção de vértices, arestas e faces que define a forma de um objeto 3D.
  ##- Funções Comuns: Manipulação e renderização de malhas, transformações geométricas.