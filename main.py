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
    mat_cubo = Material(diffuse=(0, 0, 240), specular=(255, 255, 255), reflection_color=(0, 0, 0), transparency_color=(0, 0, 0), shininess=256) # Material roxo
    mat_piramide = Material(diffuse=(255, 0, 0), specular=(255, 255, 255), reflection_color=(0, 0, 0), transparency_color=(0, 0, 0), shininess=512) # Material dourado
    mat_esfera_vermelha = Material(diffuse=(255, 0, 0), specular=(255, 255, 255), reflection_color=(0, 0, 0), transparency_color=(60, 60, 60), shininess=256)
    mat_esfera_azul = Material(diffuse=(0, 0, 255), specular=(255, 255, 255), reflection_color=(200, 200, 200), transparency_color=(60, 60, 60), shininess=256)
    #parede_amarela = Material(diffuse=(255, 255, 51), specular=(10, 10, 10), shininess=64, is_checkerboard=False)
    #cena.add(Plane(point=Point(5, 0, 0), normal=Vector(-0.1, 0, 0), material=parede_amarela))

    # Esfera espelhada
    mat_espelho = Material(diffuse=(102, 0, 204), # Um espelho real tem cor difusa escura
                           specular=(255, 255, 255),
                           shininess=256,
                           reflection_color=(255, 255, 255),
                           transparency_color=(255, 255, 255))
    #cena.add(Sphere(material=mat_espelho))


    mat_luz = Material(
        diffuse=(255, 255, 255),
        emission_color=(255, 255, 220)
    )
    cor_luz = (255, 255, 255)

    v0 = Point(2, 3, -2)  # Canto inferior esquerdo
    v1 = Point(-2, 3, 2)  # Canto inferior direito
    v2 = Point(-2, 6, 2)  # Canto superior direito
    v3 = Point(2, 6, -2)  # Canto superior esquerdo
    vertices_luz = [v0, v1, v2, v3]

    # Usa os 4 vértices para calcular tudo.
    # Calcula os parâmetros da luz a partir dos vértices
    posicao_luz = v0.midpoint(v2)                     # Centro do painel
    vec_u = v1 - v0                                   # Vetor da largura
    vec_v = v3 - v0                                   # Vetor da altura
    direcao_luz = vec_u.cross_product(vec_v).normalize() # Normal aponta para "fora" do painel

    # Cria a fonte de luz invisível
    luz_retangular = RectangularLight(
        position=posicao_luz,
        direction=direcao_luz,
        u_vec=vec_u,
        v_vec=vec_v,
        intensity=cor_luz
    )
    cena.add_light(luz_retangular)

    # Cria o objeto físico usando os vértices definidos
    quad_luz = Mesh(
        vertices=vertices_luz, 
        faces=[(0, 1, 2), (0, 2, 3)],
        material=mat_luz
    )
    cena.add_mesh(quad_luz)

    cena.add(Plane(point=Point(0, -1, 0), normal=Vector(0, 1, 0), material=mat_chao_xadrez)) # Adiciona um plano (chão)
    

    transform_esfera1 = Matrix4.translation(0, 0, 0)
    esfera1 = Sphere(material=mat_esfera_vermelha, transform=transform_esfera1)
    #cena.add(esfera1)

    transform_esfera2 = Matrix4.translation(1.5, 0, 0)
    esfera2 = Sphere(material=mat_esfera_azul, transform=transform_esfera2)
    #cena.add(esfera2)

    # cena.add_light(Light(Point(10, 20, -20), intensity=(255, 255, 255))) # Luz branca
    # cena.add_light(Light(Point(-15, 15, -5), intensity=(100, 150, 255))) # Luz azulada


    # CARREGANDO UM MODELO .OBJ
    print("Carregando modelo .obj...")
    try:
        # Cubo
        verts, faces = load_obj_file("modelos/cubo2.obj")
        transformacao_cubo = Matrix4.rotation_y(60) * Matrix4.translation(-2.5, 0, -1.5)
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