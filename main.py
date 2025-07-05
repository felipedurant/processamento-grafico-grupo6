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

def main():
    print("Iniciando a configuração da cena...")

    # 2. DEFINIÇÃO DOS MATERIAIS
    # É uma boa prática definir os materiais primeiro.
    mat_chao_xadrez = Material(color=(255, 255, 255), ambient=0.2, diffuse=0.8, specular=0.2, shininess=64, reflection=0.1, is_checkerboard=True)
    mat_esfera_vermelha = Material(color=(255, 0, 0), ambient=0.2, diffuse=0.9, specular=0.9, shininess=256, reflection=0.3)
    mat_esfera_azul = Material(color=(0, 0, 255), ambient=0.2, diffuse=0.6, specular=0.9, shininess=256, reflection=0.5, transparency=0.3, ior=1.5)
    mat_malha_verde = Material(color=(0, 255, 0), ambient=0.2, diffuse=0.8, specular=0.5, shininess=128)

    # 3. DEFINIÇÃO DA CENA (LISTA DE OBJETOS)
    # A cena é um objeto da classe Scene, que contém a lista de objetos e luzes.
    cena = Scene()

    # Adiciona um plano (chão)
    cena.add(Plane(point=Point(0, -1, 0), normal=Vector(0, 1, 0), material=mat_chao_xadrez))

    # Adiciona esferas
    cena.add(Sphere(center=Point(-7, 0, 3), radius=1.0, material=mat_esfera_vermelha))
    cena.add(Sphere(center=Point(1.5, -1, -0.5), radius=1.0, material=mat_esfera_azul))

    # Adiciona uma malha (um tetraedro, como no seu exemplo)
    vertices_tetra = [Point(0, 2, 3), Point(1, 0, 2), Point(-1, 0, 2), Point(0, 0, 4)]
    faces_tetra = [(0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 3, 2)]
    malha = Mesh(vertices_tetra, faces_tetra, mat_malha_verde)
    cena.add_mesh(malha) # O método add_mesh adiciona todos os triângulos da malha na cena

    # Adiciona fontes de luz
    cena.add_light(Point(5, 5, -5))
    cena.add_light(Point(-5, 10, -5))

    # CARREGANDO UM MODELO .OBJ
    print("Carregando modelo .obj...")
    try:
        # Especifique o caminho para o seu arquivo .obj
        # Você pode baixar modelos de sites como TurboSquid ou criar no Blender.
        verts, faces = load_obj_file("modelos/suzanne.obj") 
        
        # Crie um material para o seu modelo
        mat_macaco = Material(color=(218, 165, 32), shininess=1000, reflection=0.2) # Dourado

        # Use nossa classe Mesh para processar os dados
        modelo_obj = Mesh(vertices=verts, faces=faces, material=mat_macaco)

        # Adicione a malha completa (todos os seus triângulos) à cena
        cena.add_mesh(modelo_obj)
        print("Modelo .obj adicionado à cena com sucesso.")
        
    except FileNotFoundError:
        print("AVISO: Modelo .obj não encontrado. Renderizando sem ele.")
    except Exception as e:
        print(f"AVISO: Falha ao carregar modelo .obj: {e}. Renderizando sem ele.")

    # 4. CONFIGURAÇÃO DA CÂMERA
    # Usando a nova assinatura com FOV (campo de visão).
    largura = 800
    altura = 600
    minha_camera = Camera(
        position=Point(0, 2, -5),
        target=Point(0, 0, 0),
        screen_width=largura,
        screen_height=altura,
        fov_degrees=75.0
    )

    # 5. CONFIGURAÇÃO E EXECUÇÃO DO RENDERER
    # O Renderer recebe a câmera e a cena.
    meu_renderer = Renderer(camera=minha_camera, scene=cena)

    print("Renderizador configurado. Iniciando renderização...")
    # O método render() retorna um objeto Image.
    imagem_final = meu_renderer.render()

    # 6. SALVANDO A IMAGEM
    # O objeto Image cuida de salvar no formato correto.
    imagem_final.save("render_final.png")

if __name__ == "__main__":
    main()