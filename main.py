from point import Point
from vector import Vector
from material import Material
from camera import Camera
from renderer import Renderer
from scene import Scene, Light
from obj_loader import load_obj_file

from sphere import Sphere
from plane import Plane
from mesh import Mesh
from matrix import Matrix4

def main():
    print("Iniciando a configuração da cena...")
    # A cena é um objeto da classe Scene, que contém a lista de objetos e luzes.
    cena = Scene(ambient_light=(30, 30, 30))

    largura = 800
    altura = 600
    minha_camera = Camera(
        position=Point(0, 2, -5),
        target=Point(0, 0, 0),
        screen_width=largura,
        screen_height=altura,
        fov_degrees=75.0
    )

    meu_renderer = Renderer(camera=minha_camera, scene=cena, max_depth=3)

    print("Renderizador configurado. Iniciando renderização...")


    # DEFINIÇÃO DOS MATERIAIS
    mat_chao_xadrez = Material(diffuse=(200, 200, 200), is_checkerboard=True)
    mat_cubo = Material(diffuse=(102, 0, 204), specular=(255, 255, 255), reflection_color=(100, 100, 100), transparency_color=(60, 60, 60), shininess=256) # Material roxo
    mat_piramide = Material(diffuse=(212, 175, 55), specular=(255, 255, 255), reflection_color=(100, 100, 100), transparency_color=(60, 60, 60), shininess=512) # Material dourado
    mat_esfera_vermelha = Material(diffuse=(255, 0, 0), specular=(255, 255, 255), reflection_color=(200, 200, 200), shininess=256)
    mat_esfera_azul = Material(diffuse=(0, 0, 255), specular=(255, 255, 255), shininess=256)
    #parede_amarela = Material(diffuse=(255, 255, 51), specular=(10, 10, 10), shininess=64, is_checkerboard=False)
    #cena.add(Plane(point=Point(5, 0, 0), normal=Vector(-0.1, 0, 0), material=parede_amarela))

    # Esfera espelhada
    mat_espelho = Material(diffuse=(50, 50, 80), # Um espelho real tem cor difusa escura
                           specular=(255, 255, 255),
                           shininess=1000,
                           reflection_color=(230, 230, 230),
                           transparency_color=(60, 60, 60),)

    
    cena.add_light(Light(Point(10, 20, -20), intensity=(255, 255, 255))) # Luz branca
    cena.add_light(Light(Point(-15, 15, -5), intensity=(100, 150, 255))) # Luz azulada
    cena.add(Plane(point=Point(0, -1, 0), normal=Vector(0, 1, 0), material=mat_chao_xadrez)) # Adiciona um plano (chão)


    cena.add(Sphere(material=mat_espelho))

    transform_esfera1 = Matrix4.translation(-1.5, 0, 2)
    esfera1 = Sphere(material=mat_esfera_vermelha, transform=transform_esfera1)
    #cena.add(esfera1)

    transform_esfera2 = Matrix4.translation(3, 0, 0)
    esfera2 = Sphere(material=mat_esfera_azul, transform=transform_esfera2)
    #cena.add(esfera2)


    # CARREGANDO UM MODELO .OBJ
    print("Carregando modelo .obj...")
    try:
        # Cubo
        verts, faces = load_obj_file("modelos/cubo2.obj")
        transformacao_cubo = Matrix4.rotation_y(45) * Matrix4.translation(-2.5, 0, -1.5)
        vertices_transformados = [transformacao_cubo * v for v in verts]
        cubo = Mesh(vertices=vertices_transformados, faces=faces, material=mat_cubo)
        cena.add_mesh(cubo)
        print("Modelo .obj adicionado à cena com sucesso.")

        # Piramide
        verts, faces = load_obj_file("modelos/piramide.obj")
        transform_piramide = Matrix4.translation(2.5, 0, -1.5) * Matrix4.rotation_y(30)
        vertices_transformados = [transform_piramide * v for v in verts]
        piramide = Mesh(vertices=vertices_transformados, faces=faces, material=mat_piramide)
        cena.add_mesh(piramide)
        print("Modelo piramide.obj adicionado à cena.")

        
    except FileNotFoundError:
        print("AVISO: Modelo .obj não encontrado. Renderizando sem ele.")
    except Exception as e:
        print(f"AVISO: Falha ao carregar modelo .obj: {e}. Renderizando sem ele.")


    imagem_final = meu_renderer.render()
    imagem_final.save("render_final.png")


if __name__ == "__main__":
    main()