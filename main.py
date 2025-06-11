from obj_reader import ObjReader
from point import Point
from vector import Vector
from camera import Camera
from sphere import Sphere
from scene import Scene
from color_map import Material
from color_map import Colormap

def main():
    print("Iniciando o Ray Caster...")

    # 1. Configurar a Câmera
    # C: Localização da câmera
    # M: Ponto para onde a câmera aponta (centro da tela)
    # V_up: Vetor "para cima" da câmera
    # d: Distância da câmera à tela
    # camera_h_res, camera_v_res: Resolução da tela em pixels
    camera_C = Point(0.0, 0.0, 0.0)
    camera_M = Point(0.0, 0.0, 1.0) # Aponta para frente ao longo do eixo Z positivo
    camera_V_up = Vector(0.0, 1.0, 0.0) # Y positivo é "para cima"
    camera_d = 1.0 # Distância da câmera à tela
    camera_h_res = 800 # Largura da imagem em pixels
    camera_v_res = 600 # Altura da imagem em pixels
    
    camera = Camera(camera_C, camera_M, camera_V_up, camera_d, camera_h_res, camera_v_res)
    print(f"Câmera configurada: Resolução {camera_h_res}x{camera_v_res}")

    # 2. Definir Materiais de Teste
    # Cores normalizadas entre 0 e 1
    # Material Vermelho
    material_red = Material() # Cria uma instância do Material sem argumentos
    material_red.ka = Vector(0.0, 0.0, 0.0)    # Ambiente (ignorado por enquanto)
    material_red.kd = Vector(1.0, 0.0, 0.0)    # Difusa (cor principal da esfera)
    material_red.ks = Vector(0.0, 0.0, 0.0)    # Especular (brilho, ignorado por enquanto)
    material_red.ke = Vector(0.0, 0.0, 0.0)    # Emissiva (luz própria, ignorado por enquanto)
    material_red.ns = 0.0                      # Brilho (Ns)
    material_red.ni = 0.0                      # Densidade óptica (Ni)
    material_red.d = 1.0                       # Dissolução (d)

    # Material Verde
    material_green = Material()
    material_green.ka = Vector(0.0, 0.0, 0.0)
    material_green.kd = Vector(0.0, 1.0, 0.0)
    material_green.ks = Vector(0.0, 0.0, 0.0)
    material_green.ke = Vector(0.0, 0.0, 0.0)
    material_green.ns = 0.0
    material_green.ni = 0.0
    material_green.d = 1.0

    # Material Azul
    material_blue = Material()
    material_blue.ka = Vector(0.0, 0.0, 0.0)
    material_blue.kd = Vector(0.0, 0.0, 1.0)
    material_blue.ks = Vector(0.0, 0.0, 0.0)
    material_blue.ke = Vector(0.0, 0.0, 0.0)
    material_blue.ns = 0.0
    material_blue.ni = 0.0
    material_blue.d = 1.0

    # 3. Criar Objetos (Esferas)
    sphere1 = Sphere(Point(0.0, 1.0, 5.0), 1.0, material_red) # Esfera vermelha próxima do centro
    sphere2 = Sphere(Point(-1.5, -0.5, 3.5), 0.7, material_green) # Esfera verde à esquerda/baixo
    sphere3 = Sphere(Point(0.0, 0.0, 1.5), 0.5, material_blue) # Esfera azul à direita/cima

    # 4. Configurar a Cena
    scene = Scene(camera, [sphere1, sphere2, sphere3])
    print(f"Cena configurada com {len(scene.objects)} objetos.")

    # 5. Inicializar o Canvas (matriz de pixels para armazenar as cores)
    # Cada pixel armazenará uma lista de 3 floats [R, G, B]
    image_data = [[Vector(0.0, 0.0, 0.0) for _ in range(camera_h_res)] for _ in range(camera_v_res)]
    print(f"Canvas inicializado com {camera_v_res}x{camera_h_res} pixels.")

    # 6. Loop Principal de Renderização
    print("Iniciando renderização...")
    for y in range(camera_v_res):
        for x in range(camera_h_res):
            # Obtém a posição 3D do pixel na tela
            pixel_world_pos = camera.get_pixel_world_position(x, y)
            
            # Calcula a direção do raio da câmera para o pixel
            ray_direction = camera.get_ray_direction(pixel_world_pos)

            # Para cada raio, encontrar a interseção mais próxima com qualquer objeto na cena
            closest_t = float('inf') # Infinito para encontrar o t mais próximo
            hit_object = None # O objeto que foi atingido

            for obj in scene.objects:
                t = obj.intersect(camera.C, ray_direction)
                
                # Se houve interseção e é a mais próxima até agora
                if t is not None and t < closest_t:
                    closest_t = t
                    hit_object = obj

            # Atribui a cor ao pixel
            if hit_object:
                # Se atingiu um objeto, use a cor difusa do material desse objeto
                image_data[y][x] = hit_object.material.kd
            else:
                # Se não atingiu nada, cor de fundo (azul céu)
                # Cores normalizadas [0,1]
                background_color = Vector(0.5, 0.7, 1.0) # Um tom de azul claro
                image_data[y][x] = background_color
        
        # Opcional: Mostrar progresso a cada 10% da imagem
        if (y * 100) % camera_v_res == 0:
            print(f"Progresso: {((y / camera_v_res) * 100):.0f}%")
            
    print("Renderização concluída!")

    # 7. Salvar a Imagem como um arquivo .ppm
    output_filename = "output.ppm"
    with open(output_filename, 'w') as f:
        # Cabeçalho PPM (P3 = RGB ASCII, largura altura, valor máximo de cor)
        f.write(f"P3\n")
        f.write(f"{camera_h_res} {camera_v_res}\n")
        f.write(f"255\n") # Valor máximo para cada componente de cor (0-255)

        for y in range(camera_v_res):
            for x in range(camera_h_res):
                color_vector = image_data[y][x]
                
                # Converte os floats [0,1] para inteiros [0,255]
                # Garante que os valores não excedam 255 (clamp)
                r = int(min(255, max(0, color_vector.x * 255)))
                g = int(min(255, max(0, color_vector.y * 255)))
                b = int(min(255, max(0, color_vector.z * 255)))
                
                f.write(f"{r} {g} {b} ")
            f.write("\n") # Nova linha após cada linha de pixels

    print(f"Imagem salva como '{output_filename}'")

if __name__ == "__main__":
    main()