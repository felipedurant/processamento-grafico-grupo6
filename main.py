from image import *
from camera import *
from plane import *
from sphere import *
from mesh import *
from transform import translate, rotate_y, apply_to_point

# Camera:
width = 200
heigth = 200
c = Camera(position=Point(1, 0, 0), target=Point(-20, 0, 0), screen_distance=20, screen_heigth=heigth, screen_width=width)

# plano
p = Plane(Point(0, 0, -10), Vector(0, 0, 1), Material((0, 255, 0)))

def gerar_imagem_longe_da_camera():
    # Esfera longe da câmera:
    s = Sphere(Point(-60, 0, 0), 30, (255, 0, 0))

    # Matriz de cores:
    matrix = c.start_ray_cast([p, s])

    # Gerar imagem:
    generate_image(matrix, width, heigth, "Imagem_longe_da_camera")

def gerar_imagem_perto_da_camera():
    # Esfera perto da câmera:
    s = Sphere(Point(-30, 0, 0), 30, (255, 0, 0))

    # Matriz de cores:
    matrix = c.start_ray_cast([p, s])

    # Gerar imagem:
    generate_image(matrix, width, heigth, "Imagem_perto_da_camera")

def gerar_imagem_esquerda_e_acima():
    # Esfera a esquerda e acima:
    s = Sphere(Point(-60, 90, 20), 30, (255, 0, 0))

    # Matriz de cores:
    matrix = c.start_ray_cast([p, s])

    # Gerar imagem:
    generate_image(matrix, width, heigth, "Imagem_esquerda_e_acima")

def gerar_imagem_direita_e_acima():
    # Esfera a direita e acima:
    s = Sphere(Point(-60, -90, 30), 30, (255, 0, 0))

    # Matriz de cores:
    matrix = c.start_ray_cast([p, s])

    # Gerar imagem:
    generate_image(matrix, width, heigth, "Imagem_direita_e_acima")

 
def gerar_imagem_dois_circulos():
    # Esfera a direita e acima:
    s1 = Sphere(Point(-60, -90, 20), 30, (255, 0, 0))
    s2 = Sphere(Point(-60, 90, 20), 30, (255, 0, 0))

    # Matriz de cores:
    matrix = c.start_ray_cast([p, s1, s2])

    # Gerar imagem:
    generate_image(matrix, width, heigth, "Imagem_dois_circulos")

def gerar_imagem_planos():
    #Planos:
    plano1 = Plane(Point(0, -20, 0), Vector(0, 1, 0), Material((0, 0, 255)))
    plano2 = Plane(Point(0, 20, 0), Vector(0, 1, 0), Material((0, 0, 255)))
    plano3 = Plane(Point(-12, 0, 0), Vector(1, 0, 0), Material((0, 255, 255)))

    # Matriz de cores:
    matrix = c.start_ray_cast([p, plano1, plano2, plano3])

    # Gerar imagem:
    generate_image(matrix, width, heigth, "Imagem_planos_laterais")
    
def gerar_imagem_malha():
    material = Material((255, 0, 0))  # vermelho
    mesh = Mesh("cube.obj", material)

    # Aplicar transformação
    transform = translate(0, 0, -5) @ rotate_y(1.57)
    mesh.vertices = [apply_to_point(transform, v) for v in mesh.vertices]

    # Adicionar plano para fundo
    p = Plane(Point(0, 0, -10), Vector(0, 0, 1), Material((0, 255, 0)))

    # Ray cast
    matrix = c.start_ray_cast([p, mesh])
    generate_image(matrix, width, heigth, "Imagem_malha")
    
    transform = translate(0, 0, -5) @ rotate_y(1.57)
    mesh.vertices = [apply_to_point(transform, v) for v in mesh.vertices]
    generate_image(c.start_ray_cast([mesh]), width, heigth, "Imagem_com_transformacao")

gerar_imagem_longe_da_camera()
gerar_imagem_perto_da_camera()
gerar_imagem_esquerda_e_acima()
gerar_imagem_direita_e_acima()
gerar_imagem_dois_circulos()
gerar_imagem_planos()
gerar_imagem_malha()

### Classe "Main"
 ## - Propósito: contém o ponto de entrada do programa, gerenciando a inicialização e execução do pipeline de renderização.
 ## - Funções Comuns: Configuração inicial, execução do loop principal do aplicativo.
