from typing import Optional
from camera import Camera
from object import Object
from ray import Ray
from image import Image
from scene import Scene
from math import floor, pow


# Função auxiliar para manipular cores (somar e multiplicar)
def add_colors(c1, c2):
    return (c1[0] + c2[0], c1[1] + c2[1], c1[2] + c2[2])

def multiply_color_by_scalar(c, s):
    return (c[0] * s, c[1] * s, c[2] * s)

"""
Classe responsável por renderizar a cena
"""
class Renderer:
    def __init__(self, camera: Camera, scene: Scene, background_color: tuple = (0, 0, 0)):
        self.camera = camera
        self.scene = scene
        self.background_color = background_color
        
    def find_closest_intersection(self, ray: Ray) -> Optional[tuple]:
        """
        Testa a interseção de um raio com todos os objetos da cena.

        Retorna:
            Uma tupla (distancia, objeto) da interseção mais próxima, ou None.
        """
        closest_distance = float('inf')
        closest_object = None

        for obj in self.scene.objects:
            distance = obj.intersects(ray)
            if distance is not None and distance < closest_distance:
                closest_distance = distance
                closest_object = obj
        
        if closest_object:
            return (closest_distance, closest_object)
        return None
    
    def shade(self, obj: Object, hit_point, normal, ray: Ray) -> tuple:
        """
        Calcula a cor final de um ponto usando o modelo de iluminação de Phong.
        """
        material = obj.material

        # INÍCIO DA LÓGICA DO XADREZ
        # Verifica se o material do objeto é do tipo xadrez
        if material.is_checkerboard:
            check = (floor(hit_point.x) + floor(hit_point.z)) % 2
            if check == 0:
                base_color = material.color # Cor 1 (ex: branco)
            else:
                base_color = (20, 20, 20)  # Cor 2 (ex: preto/cinza escuro)
        else:
            # Comportamento normal: se não for xadrez, usa a cor sólida do material
            base_color = material.color
        # FIM DA LÓGICA DO XADREZ


        # Inicia a cor final com a contribuição da luz ambiente
        final_color = multiply_color_by_scalar(material.color, material.ambient)

        # 2. Loop sobre todas as fontes de luz para calcular Difusa e Especular
        for light in self.scene.lights:
            light_dir = (light - hit_point).normalize()

            # CÁLCULO DE SOMBRA
            # Lança um raio de sombra para verificar se o ponto está obstruído da luz
            shadow_ray_origin = hit_point + normal * obj.shadow_bias
            shadow_ray = Ray(shadow_ray_origin, light_dir)
            shadow_hit = self.find_closest_intersection(shadow_ray)
            
            # Se o raio de sombra atingir qualquer objeto, o ponto está na sombra
            # em relação a ESTA fonte de luz, então pulamos para a próxima luz.
            if shadow_hit is not None:
                continue
            # FIM DO CÁLCULO DE SOMBRA

            # 3. Componente Difusa
            # Mede o quão de frente a superfície está para a luz
            diffuse_intensity = max(0, normal.dot_product(light_dir))
            diffuse_color = multiply_color_by_scalar(base_color, material.diffuse * diffuse_intensity)
            final_color = add_colors(final_color, diffuse_color)

            # 4. Componente Especular
            # Mede o quão alinhado o reflexo da luz está com a visão da câmera
            view_dir = (ray.origin - hit_point).normalize()
            reflection_dir = (-light_dir).reflect(normal)
            specular_intensity = max(0, view_dir.dot_product(reflection_dir))
            
            if specular_intensity > 0:
                specular_power = pow(specular_intensity, material.shininess)
                # A cor do brilho especular é geralmente branca (ou a cor da luz)
                specular_color = multiply_color_by_scalar((255, 255, 255), material.specular * specular_power)
                final_color = add_colors(final_color, specular_color)

        # Garante que os valores de cor não ultrapassem 255
        final_color = (min(255, final_color[0]), min(255, final_color[1]), min(255, final_color[2]))

        return final_color
    
    def render(self) -> Image:
        """
        Renderiza a cena inteira e retorna um objeto Image.
        """
        # 1. Cria o objeto de imagem que será preenchido
        final_image = Image(self.camera.screen_width, self.camera.screen_height)

        for y in range(self.camera.screen_height):
            for x in range(self.camera.screen_width):
                ray = self.camera.generate_ray_for_pixel(x, y)
                hit = self.find_closest_intersection(ray)
                
                color = self.background_color
                if hit:
                    distance, obj_hit = hit
                    hit_point = ray.point_at(distance)
                    local_hit_point = obj_hit.inverse_transform * hit_point
                    local_normal = obj_hit.get_normal_at(local_hit_point)
                    material = obj_hit.material

                    world_normal = (obj_hit.inverse_transform_transpose * local_normal).normalize()
                    # Se atingiu algo, calcula a cor com base na luz e sombra
                    color = self.shade(obj_hit, hit_point, world_normal, ray)

                                    
                # 2. Define o pixel diretamente no objeto de imagem
                final_image.set_pixel(x, y, color)
        
        # 3. Retorna o objeto de imagem completo
        print("Renderização concluída!")
        return final_image