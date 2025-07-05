from point import Point
from vector import Vector
from ray import Ray
from math import tan, radians

class Camera:
    def __init__(self, position: Point, target: Point, screen_height: int, screen_width: int,
                fov_degrees: float=60.0, up_vector: Vector = Vector(0, 1, 0)):
        """
        Inicializa a câmera, a posicionando e definindo seus valores.

        Args:
        position (Point): ponto em que a câmera está. 
        target (Point): ponto para o qual a câmera está olhando.
        screen_heigth (int): altura da tela.
        screen_width (int): largura da tela.
        fov_degrees (float): Campo de visão vertical, em graus.
        up_vector (Vector): vetor que indica a direção "para cima" do mundo.
        """
        # Posições:
        self.position = position
        self.target = target
        self.screen_height = max(1, screen_height)
        self.screen_width = max(1, screen_width)

        # 1. Cria a base ortonormal da câmera (u, v, w)
        # w aponta da cena PARA a câmera
        self.w = (position - target).normalize()
        # u aponta para a direita da câmera
        self.u = up_vector.cross_product(self.w).normalize()
        # v aponta para cima da câmera
        self.v = self.w.cross_product(self.u)

        # 2. Calcula as dimensões da "tela" virtual no espaço 3D
        aspect_ratio = self.screen_width / self.screen_height
        # A altura da tela virtual é baseada no FOV
        viewplane_height = 2 * tan(radians(fov_degrees) / 2)
        viewplane_width = aspect_ratio * viewplane_height

        # 3. Vetores para percorrer a tela virtual
        self.horizontal_step = self.u * (viewplane_width / self.screen_width)
        self.vertical_step = self.v * (viewplane_height / self.screen_height)

        # 4. Posição do canto inferior esquerdo da tela virtual
        # Primeiro, encontramos o centro da tela e depois nos movemos para o canto
        center_point = self.position - self.w
        self.bottom_left_corner = center_point - (self.u * (viewplane_width / 2)) - (self.v * (viewplane_height / 2))

    def generate_ray_for_pixel(self, x: int, y: int) -> Ray:
        """
        Gera um novo raio que passa pelo centro do pixel (x, y).
        """
        # Calcula a direção para o pixel específico
        target_point = self.bottom_left_corner + \
                    self.horizontal_step * (x + 0.5) + \
                    self.vertical_step * (y + 0.5)
        
        direction = (target_point - self.position).normalize()
        
        # Retorna um NOVO objeto Ray, sempre seguro e normalizado
        return Ray(self.position, direction)


### Classe "Camera"
 ## - Propósito: Gerencia a perspectiva ou visão da cena 3D. Pode definir a posição, orientação e parâmetros de projeção da câmera.
## - Funções Comuns: Ajuste de posição e direção da câmera, configuração de projeção (perspectiva ou ortográfica).

