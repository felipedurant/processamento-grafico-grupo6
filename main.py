from image import *
from camera import *
from plane import *
from sphere import *
from mesh import *
from material import *

# Camera:
width = 600
heigth = 450
c = Camera(position=Point(60, 20, 20), target=Point(0, 30, 0), screen_distance=100, screen_heigth=heigth, screen_width=width)

# Objetos:
p = Plane(Point(0, 0, -10), Vector(0, 0, 1), Material((0, 255, 0)))
vertices = [Point(0, 0, 50), Point(40, 0, 0), Point(0, 25, 0), Point(0, -25, 0)]
triplas = [(0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 2, 3)]
m = Mesh(vertices, triplas, 4, 4, (255, 0, 0))

# Matriz de cores:
matrix = c.start_ray_cast([p, m])

# Gerar imagem:
generate_image(matrix, width, heigth, "Imagem")

### Classe "Main"
 ## - Propósito: contém o ponto de entrada do programa, gerenciando a inicialização e execução do pipeline de renderização.
 ## - Funções Comuns: Configuração inicial, execução do loop principal do aplicativo.
