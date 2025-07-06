from vector import *
from point import *
from object import *
from ray import *
from math import *

class Camera:
    def __init__(self, position : Point, target : Point, screen_distance : float,
                 resolution_height : int, resolution_width  : int, up_vector : Vector =Vector(0,0,1)):
        """
        Inicializa a câmera, a posicionando e definindo seus valores.

        Args:
        position (Point): ponto em que a câmera está. 
        target (Point): ponto para o qual a câmera está olhando.
        screen_distance (float): distancia entre a câmera e a tela.
        resolution_height (int): altura da tela.
        resolution_width (int): largura da tela.
        up_vector (Vector): vetor que aponta para cima.
        """
        # Posições:
        self.position : Point = position
        self.target : Point = target
        #Screen:
        self.scr_dist : float = screen_distance
        self.res_h : int = self.set_resolution_height(resolution_height)
        self.res_w : int = self.set_resolution_width(resolution_width)
        self.scr_size_x : float = 50
        self.scr_size_y : float = 37.5
        # Vectors:
        self.vec_target : Vector = self.get_target_vector().normalize()
        self.vec_up : Vector = self.set_vector_up(up_vector)
        self.vec_u : Vector = self.vec_target.cross_product(self.vec_up).normalize()
        self.vec_v : Vector = self.vec_target.cross_product(self.vec_u).normalize()
        self.vec_w : Vector = -self.vec_target.normalize()
        self.vec_qx : Vector = self.scr_size_x/(self.res_w) * self.vec_u
        self.vec_qy : Vector = self.scr_size_y/(self.res_h) * self.vec_v
        # Ray
        self.ray : Ray = Ray(self.position, Vector())
        self.current_pixel = [0,0]

    def get_target_vector(self):
        """
        Retorna o vetor que vai da posicão da câmera até a posição do target.
        
        Returns:
        Vector: vetor formado pela diferença entre o ponto do target e o ponto da posição da câmera.
        """
        return self.target - self.position

    def set_resolution_height(self, heigth : int):
        """
        Define o valor da altura da tela.
        Se o valor recebido for menor ou igual a zero, a altura é definida como 1.

        Args:
        heigth (int): valor da altura da tela; deve ser maior que zero.

        Returns:
        int: altura da tela.
        """
        if heigth <= 0:
            self.res_h = 1
        else:
            self.res_h = heigth
        return self.res_h
    
    def set_resolution_width(self, width : int):
        """
        Define o valor da largura da tela.
        Se o valor recebido for menor ou igual a zero, a largura é definida como 1.

        Args:
        width (int): valor da largura da tela; deve ser maior que zero.

        Returns:
        int: largura da tela.
        """
        if width <= 0:
            self.res_w = 1
        else:
            self.res_w = width
        return self.res_w

    def set_vector_up(self, vector : Vector):
        """
        Define o vector up da câmera, normalizando o vetor recebido como parametro.
        Se vetor for nulo, vetor up será Vector(0, 0, 1).

        Args:
        vector (Vector): vetor que será e passado para o vec_up.

        Returns:
        Vector: vetor que foi definido como vector up da câmera.
        """
        if vector != Vector(0, 0, 0):
            self.vec_up = vector.normalize()
        else:
            self.vec_up = Vector(0, 0, 1)
        return self.vec_up

    def put_ray_in_start_position(self):
        """Faz o ray apontar para o centro do pixel que fica no topo esquerdo da tela (cordenada (0, 0))."""
        # Muda a direção do ray para um vetor (0, 0, 0) e as cordenadas do pixel atual em (0, 0).
        self.ray.set_direction(Vector())
        self.current_pixel = [0,0]
        # Faz a direção do ray apontar para o topo esquerdo da tela:
        self.ray.change_direction((self.vec_w.invert() * self.scr_dist)) # ray aponta para o centro da tela.
        self.ray.change_direction((self.vec_v * -(self.scr_size_y/2))) # ray aponta para o topo da tela.
        self.ray.change_direction((self.vec_u * -(self.scr_size_x/2))) # ray aponta para o topo esquerdo da tela.
        # Posiciona o ray no centro do pixel:
        pixel_size_x = self.scr_size_x/self.res_w
        pixel_size_y = self.scr_size_y/self.res_h
        # Faz o ray apontar para o centro do pixel (horizontalmente):
        if self.res_w % 2 == 0:
            self.ray.change_direction((self.vec_u * (pixel_size_x/2)))
        # Faz o ray apontar para o centro do pixel (verticalmente):
        if self.res_h % 2 == 0:
            self.ray.change_direction((self.vec_v * (pixel_size_y/2)))
    
    def start_ray_cast(self, objects : list):
        """
        Começa a fazer o processo de raycast, fazendo o raio passar por todos os pixels da tela e verificar se está
        atingindo algum objeto e dando a aquele pixel a cor do objeto atingido mais proximo.
        
        Args:
        objects (list): Lista de objetos que podem (ou não) colidir com o raio.

        Returns:
        matriz ([[(r, g, b)]]): Matriz com as cores dos pixels da tela.
        """
        objects = self.clean_objects_list(objects)
        screen_matrix = []
        self.put_ray_in_start_position()
        start_direction : Vector = self.ray.get_direction()
        for y in range(self.res_h):
            screen_matrix.append([])
            for x in range(self.res_w):
                self.ray.set_direction((start_direction + (x * self.vec_qx) + (y * self.vec_qy)))
                self.current_pixel = [x, y]
                intercections = self.verify_intersections(objects)
                closest = self.get_closest_object(intercections)
                if closest != None:
                    screen_matrix[y].append(intercections[closest]["color"])
                else: 
                    screen_matrix[y].append(None)
        return screen_matrix

    @staticmethod
    def clean_objects_list(objects_list : list):
        clean_list = []
        for o in objects_list:
            if isinstance(o, Object):
                clean_list.append(o)
        return clean_list


    def verify_intersections(self, objects : list):
        """
        Verifica se o raio colide com os objetos de uma lista de objetos.

        Args:
        ray (Ray): Raio o qual a colisão será verificada.
        objects (list): Lista de objetos que podem (ou não) colidir com o raio.

        Returns:
        dict: Dicionario que contem como chave os objetos que colidiram com o raio e como valores as informações da colisão.
        """
        intersection_info = None
        intersections_dict = {}
        for obj in objects:
            intersection_info = obj.intersects(self.ray)
            if intersection_info != None:
                intersections_dict[obj] = intersection_info
        return intersections_dict
    
    @staticmethod
    def get_closest_object(intercetion_dict : dict):
        """
        Determina quais dos objetos está mais proximo do ponto de origem, a partir do parametro t
        que determina que ponto do raio bateu no objeto, o que tiver o menor t é o mais proximo.
        
        Args:
        intercetion_dict (dict): Dicionario que contem os objetos e as informações de colisão.

        Returns:
        Objeto mais proximo (com o menor t).
        """
        if len(intercetion_dict.keys()) > 0:
            closest_obj = None
            distance = None
            for k in intercetion_dict.keys():
                if closest_obj == None:
                    closest_obj = k
                    distance = intercetion_dict[k]["t"]
                else:
                    if distance > intercetion_dict[k]["t"]:
                        closest_obj = k
                        distance = intercetion_dict[k]["t"]
            return closest_obj
        else:
            return None


### Classe "Camera"
 ## - Propósito: Gerencia a perspectiva ou visão da cena 3D. Pode definir a posição, orientação e parâmetros de projeção da câmera.
## - Funções Comuns: Ajuste de posição e direção da câmera, configuração de projeção (perspectiva ou ortográfica).

