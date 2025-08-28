from point import Point
from vector import Vector
from material import Material
from camera import Camera
from renderer import Renderer
from scene import Scene, Light, RectangularLight
from obj_loader import load_obj_file

from sphere import Sphere
from plane import Plane
from mesh import Mesh
from matrix import Matrix4

def main():
    print("Iniciando a configuração da cena...")
    # A cena é um objeto da classe Scene, que contém a lista de objetos e luzes.
    cena = Scene(ambient_light=(15, 15, 15))

    largura = 800
    altura = 600
    minha_camera = Camera(
        position=Point(0, 4, -10),
        target=Point(0, 1.5, 0),
        screen_width=largura,
        screen_height=altura,
        fov_degrees=60.0
    )

    meu_renderer = Renderer(camera=minha_camera, scene=cena, max_depth=4, shadow_samples=32)

    print("Renderizador configurado. Iniciando renderização...")


    # DEFINIÇÃO DOS MATERIAIS
    mat_chao_xadrez = Material(diffuse=(200, 200, 200), is_checkerboard=True)
    mat_cubo = Material(diffuse=(102, 0, 204), specular=(30, 30, 30), reflection_color=(255, 255, 255), transparency_color=(255, 255, 255), shininess=256) # Material roxo
    mat_piramide = Material(diffuse=(255, 215, 0), specular=(255, 255, 255), reflection_color=(255, 255, 255), transparency_color=(255, 255, 255), shininess=512) # Material dourado

    # Esfera espelhada
    mat_espelho = Material(diffuse=(0, 0, 0), # Um espelho real tem cor difusa escura
                           specular=(255, 255, 255),
                           shininess=1000,
                           reflection_color=(255, 255, 255),
                           transparency_color=(0, 0, 0))
    transform_espelho = Matrix4.translation(0, 0, -1)
    cena.add(Sphere(material=mat_espelho, transform=transform_espelho))

    cena.add(Plane(point=Point(0, -1, 0), normal=Vector(0, 1, 0), material=mat_chao_xadrez)) # Adiciona um plano (chão)
    cena.add_light(Light(Point(10, 20, -10), intensity=(255, 255, 255))) # Luz branca
    cena.add_light(Light(Point(-10, 15, -5), intensity=(100, 150, 255))) # Luz azulada


    # CARREGANDO UM MODELO .OBJ
    print("Carregando modelo .obj...")
    try:
        # Cubo
        verts, faces = load_obj_file("modelos/cubo2.obj")
        transformacao_cubo = Matrix4.translation(-2.5, 0, -2.5) * Matrix4.rotation_y(60)
        vertices_transformados = [transformacao_cubo * v for v in verts]
        cubo = Mesh(vertices=vertices_transformados, faces=faces, material=mat_cubo)
        
        cena.add_mesh(cubo)
        print("Modelo .obj adicionado à cena com sucesso.")

        # Piramide
        verts, faces = load_obj_file("modelos/piramide.obj")
        transform_piramide = Matrix4.translation(2.5, 0, -2.5) * Matrix4.rotation_y(0)
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