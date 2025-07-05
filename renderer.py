from typing import Optional
from camera import Camera
from object import Object
from ray import Ray
from image import Image
from scene import Scene
from math import floor

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
                    distance, obj = hit
                    material = obj.material # Futuramente, aqui entrará a iluminação

                    # INÍCIO DA LÓGICA DO XADREZ
                    
                    # Verifica se o material do objeto é do tipo xadrez
                    if material.is_checkerboard:
                        # Ponto exato da colisão no mundo
                        hit_point = ray.point_at(distance)

                        # A matemática do xadrez: somamos os "chãos" das coordenadas
                        # x e z. Se a soma for par, usamos uma cor; se for ímpar, usamos outra.
                        # Isso cria um padrão de quadrados no plano XZ (o "chão").
                        check = (floor(hit_point.x) + floor(hit_point.z)) % 2
                        
                        if check == 0:
                            # Usa a cor base do material para uma das cores do xadrez
                            color = material.color
                        else:
                            # Usa uma cor alternativa (ex: preto ou uma variação mais escura)
                            color = (20, 20, 20) 
                    else:
                        # Comportamento normal: se não for xadrez, usa a cor sólida do material
                        color = material.color
                    
                    # FIM DA LÓGICA DO XADREZ
                    
                    # (Futuramente, o cálculo de iluminação entraria aqui, modificando a 'color')
                
                # 2. Define o pixel diretamente no objeto de imagem
                final_image.set_pixel(x, y, color)
        
        # 3. Retorna o objeto de imagem completo
        return final_image