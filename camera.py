# camera.py
from point import Point
from vector import Vector
import math

class Camera:
    """
    Representa a câmera e o plano de projeção no mundo 3D.
    """
    def __init__(self, C: Point, M: Point, V_up: Vector, d: float, h_res: int, v_res: int):
        self.C = C  # Ponto de localização da câmera
        self.M = M  # Ponto para onde a câmera aponta (centro da tela)
        self.V_up = V_up  # Vetor "para cima" da câmera

        self.d = d  # Distância entre a câmera e a tela
        self.h_res = h_res  # Resolução horizontal da tela (pixels)
        self.v_res = v_res  # Resolução vertical da tela (pixels)

        # Calculando o tamanho real da tela no mundo (assumindo pixel 1x1)
        # Definimos uma altura física para a tela (ex: 2 unidades de altura)
        self.screen_physical_height = 2.0
        # A largura é calculada com base na proporção de aspecto da resolução
        self.screen_physical_width = self.screen_physical_height * (self.h_res / self.v_res)
        
        # Calcular o tamanho de um "pixel" no mundo real
        self.pixel_width_world = self.screen_physical_width / self.h_res
        self.pixel_height_world = self.screen_physical_height / self.v_res

        # Base ortonormal da câmera (W, U, V)
        # Inicializar com um vetor vazio para type hint (estava dando erro quando inicializava como None)
        self.W: Vector = Vector(0,0,0) 
        self.U: Vector = Vector(0,0,0) 
        self.V: Vector = Vector(0,0,0) 
        self._calculate_camera_basis()

        # Ponto central da tela de projeção
        self.screen_center: Point = Point(0,0,0) # Inicializa com um Point
        self._calculate_screen_center()


    def _calculate_camera_basis(self):
        """
        Calcula os vetores ortonormais W, U, V que formam a base da câmera.
        """
        # W: Aponta do ponto de mira para a câmera e é normalizado.
        # Por convenção, W tem a mesma direção de (M - C), mas sentido oposto.
        # Portanto, W = (C - M).normalize()
        """
        Possível explicação para 'normalize()' estar com aviso:
        o problema pode ser uma questão de análise estática (o linter/type checker) que está com alguma inconsistência
        ou não conseguiu reavaliar o contexto de forma completa.
        mas o código está funcionando e 'self.W' é reconhecido como um vetor e não como um ponto.
        """
        self.W = (self.C - self.M).normalize()

        # U: Vetor "para a direita" da câmera. É o produto vetorial de V_up e W, normalizado.
        # Se V_up for paralelo a W, o produto vetorial será um vetor nulo.
        # Uma forma de lidar com isso é usar um V_up padrão.
        # Para o projeto vamos assumir que V_up não é paralelo a (M-C).
        self.U = self.V_up.cross(self.W).normalize()

        # V: Vetor "para cima" na câmera, perpendicular a U e W.
        # V = W x U
        self.V = self.W.cross(self.U).normalize() # Isso garante que V seja ortogonal a U e W

        # Verifica se a normalização resultou em vetor nulo (pode acontecer se V_up for colinear com C-M)
        if self.U.length() == 0 or self.V.length() == 0:
            print("Aviso: V_up é colinear com (C-M). A base da câmera pode ser instável.")
            

    def _calculate_screen_center(self):
        """
        Calcula o ponto central da tela de projeção.
        O centro da tela está a uma distância 'd' da câmera ao longo da direção oposta a W.
        """
        self.screen_center = self.C - (self.W * self.d)

    def _calculate_top_left_pixel_origin(self):
        """
        Calcula o ponto de origem do pixel superior esquerdo na tela.
        Este é o ponto de partida para iterar sobre os pixels.
        """
        # Partimos do centro da tela.
        # Movemos para a esquerda pela metade da largura da tela (h_size / 2) * U
        # Movemos para cima pela metade da altura da tela (v_size / 2) * V
        self.top_left_pixel_origin = self.screen_center - \
                                     (self.U * (self.screen_physical_width / 2.0)) + \
                                     (self.V * (self.screen_physical_height / 2.0))

    def get_pixel_world_position(self, x: int, y: int) -> Point:
        """
        Calcula a posição 3D no mundo do centro de um pixel específico na tela.

        Args:
            x (int): Coordenada horizontal do pixel (de 0 a h_res-1).
            y (int): Coordenada vertical do pixel (de 0 a v_res-1).

        Returns:
            Point: O ponto 3D no mundo que corresponde ao centro do pixel (x, y).
        """
        # Calcular os deslocamentos a partir do centro da tela para o pixel (x,y)
        # Convertemos as coordenadas do pixel (0 a res-1) para um intervalo que
        # representa a posição relativa ao centro da tela (ex: -width/2 a width/2)

        # Deslocamento horizontal:
        # (x + 0.5) para o centro do pixel
        # - (self.h_res / 2.0) para centralizar a origem no meio da tela
        # * self.pixel_width_world para converter para unidades do mundo
        u_offset_from_center = (x + 0.5 - (self.h_res / 2.0)) * self.pixel_width_world
        
        # Deslocamento vertical:
        # (y + 0.5) para o centro do pixel
        # - (self.v_res / 2.0) para centralizar a origem no meio da tela
        # * self.pixel_height_world para converter para unidades do mundo
        # * -1.0 porque o eixo Y da imagem cresce para baixo, mas o vetor V aponta para cima
        v_offset_from_center = (y + 0.5 - (self.v_res / 2.0)) * self.pixel_height_world * -1.0

        # A posição 3D do pixel é o centro da tela mais os deslocamentos em U e V
        pixel_world_pos = self.screen_center + \
                          (self.U * u_offset_from_center) + \
                          (self.V * v_offset_from_center)
        
        return pixel_world_pos

    def get_ray_direction(self, pixel_world_position: Point) -> Vector:
        """
        Calcula a direção do raio que parte da câmera e passa pelo centro do pixel.

        Args:
            pixel_world_position (Point): A posição 3D no mundo do centro do pixel.

        Returns:
            Vector: O vetor de direção normalizado do raio.
        """
        # A direção do raio é o vetor do centro da câmera (C) até o centro do pixel.
        return (pixel_world_position - self.C).normalize()