from point import Point
from vector import Vector
from material import Material
from camera import Camera
from renderer import Renderer
from scene import Scene
from obj_loader import load_obj_file

from sphere import Sphere
from plane import Plane
from mesh import Mesh
from matrix import Matrix4

def main():
    print("Iniciando a configuração da cena...")
    # A cena é um objeto da classe Scene, que contém a lista de objetos e luzes.
    cena = Scene()

    # CONFIGURAÇÃO DA CÂMERA
    largura = 800
    altura = 600
    minha_camera = Camera(
        position=Point(0, 2, -5),
        target=Point(0, 0, 0),
        screen_width=largura,
        screen_height=altura,
        fov_degrees=75.0
    )

    # CONFIGURAÇÃO E EXECUÇÃO DO RENDERER
    # O Renderer recebe a câmera e a cena.
    meu_renderer = Renderer(camera=minha_camera, scene=cena)

    print("Renderizador configurado. Iniciando renderização...")


    # DEFINIÇÃO DOS MATERIAIS
    # É uma boa prática definir os materiais primeiro.
    mat_chao_xadrez = Material(color=(255, 255, 255), ambient=0.2, diffuse=0.8, specular=0.2, shininess=64, reflection=0.1, is_checkerboard=True)
    mat_cubo = Material(color=(102, 0, 204), reflection=0.2, specular=0.8, shininess=256) # Material roxo
    mat_esfera_vermelha = Material(color=(255, 0, 0), ambient=0.2, diffuse=0.9, specular=0.9, shininess=256, reflection=0.3)
    mat_esfera_azul = Material(color=(0, 0, 255), ambient=0.2, diffuse=0.6, specular=0.9, shininess=256, reflection=0.5, transparency=0.3, ior=1.5)
    mat_malha_verde = Material(color=(0, 255, 0), ambient=0.2, diffuse=0.8, specular=0.5, shininess=128)
    # parede_azul = Material(color=(0, 102, 204), ambient=0.2, diffuse=0.8, specular=0.2, shininess=64, reflection=0.1, is_checkerboard=False)
    # parede_amarela = Material(color=(255, 255, 51), ambient=0.2, diffuse=0.8, specular=0.2, shininess=64, reflection=0.1, is_checkerboard=False)
    # parede_laranja = Material(color=(255, 128, 0), ambient=0.2, diffuse=0.8, specular=0.2, shininess=64, reflection=0.1, is_checkerboard=False)
    # teto = Material(color=(64, 64, 64), ambient=0.2, diffuse=0.8, specular=0.2, shininess=64, reflection=0.1, is_checkerboard=False)
    
    
    cena.add_light(Point(5, 10, -10)) # Adiciona uma luz forte acima e à direita
    cena.add_light(Point(-8, 8, -2))  # Adiciona uma luz de preenchimento à esquerda
    cena.add(Plane(point=Point(0, -1, 0), normal=Vector(0, 1, 0), material=mat_chao_xadrez)) # Adiciona um plano (chão)
    #cena.add(Plane(point=Point(0, 3, 0), normal=Vector(0, -1, 0), material=teto)) # Teto
    # Paredes
    # cena.add(Plane(point=Point(0, 0, 3), normal=Vector(0, 0, -1), material=parede_azul)) # Azul
    # cena.add(Plane(point=Point(2.8, 0, 0), normal=Vector(-0.1, 0, 0), material=parede_amarela)) # Amarela
    # cena.add(Plane(point=Point(-2.8, 0, 0), normal=Vector(1, 0, 0), material=parede_laranja)) # Laranja


    # Esfera 1: movida para a posição (-1.5, 0, 3)
    transform_esfera1 = Matrix4.translation(-1.5, 0, 1) * Matrix4.scaling(2.0, 2.0, 2.0)
    esfera1 = Sphere(material=mat_esfera_vermelha, transform=transform_esfera1)
    #cena.add(esfera1)

    # Esfera 2: movida para a posição (1.5, 0, 2)
    transform_esfera2 = Matrix4.translation(1.5, 0, 2) * Matrix4.scaling(1.0, 0.5, 1.0)
    esfera2 = Sphere(material=mat_esfera_azul, transform=transform_esfera2)
    #cena.add(esfera2)

    # cena.add(Sphere(center=Point(-1, 0, -2), radius=0.4, material=mat_esfera_vermelha))
    # cena.add(Sphere(center=Point(1, 0, -2), radius=0.4, material=mat_esfera_azul))


    # Adiciona uma malha (um tetraedro)
    vertices_tetra = [Point(0, 1, 0), Point(1, -1, -1), Point(-1, -1, -1), Point(0, -1, 1)]
    faces_tetra = [(0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 2, 3)]

    transformacao_malha = Matrix4.rotation_y(45)
    vertices_transformados = [transformacao_malha * v for v in vertices_tetra]
    malha = Mesh(vertices_transformados, faces_tetra, mat_malha_verde)
    #cena.add_mesh(malha) # O método add_mesh adiciona todos os triângulos da malha na cena


    # CARREGANDO UM MODELO .OBJ
    print("Carregando modelo .obj...")
    try:
        # Especifica o caminho para o arquivo .obj
        verts, faces = load_obj_file("modelos/cubo.obj")
        transformacao_cubo = Matrix4.rotation_y(45)
        vertices_transformados = [transformacao_cubo * v for v in verts]

        # Usa a classe Mesh para processar os dados
        cubo = Mesh(vertices=vertices_transformados, faces=faces, material=mat_cubo)
        # Adiciona a malha completa (todos os triângulos) à cena
        cena.add_mesh(cubo)
        print("Modelo .obj adicionado à cena com sucesso.")
        
    except FileNotFoundError:
        print("AVISO: Modelo .obj não encontrado. Renderizando sem ele.")
    except Exception as e:
        print(f"AVISO: Falha ao carregar modelo .obj: {e}. Renderizando sem ele.")

    # O método render() retorna um objeto Image.
    imagem_final = meu_renderer.render()
    # SALVANDO A IMAGEM
    # O objeto Image cuida de salvar no formato correto.
    imagem_final.save("render_final.png")

if __name__ == "__main__":
    main()