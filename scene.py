# scene.py
from camera import Camera
from sphere import Sphere
from typing import List

class Scene:
    """
    Representa a cena 3D, contendo a câmera, os objetos e, futuramente, as luzes.

    Atributos:
        camera (Camera): A câmera da cena.
        objects (List[Sphere]): Uma lista dos objetos na cena (por enquanto, apenas esferas).
        planos ainda em desenvolvimento
    """
    def __init__(self, camera: Camera, objects: List[Sphere]):
        self.camera = camera
        self.objects = objects

    def add_object(self, obj: Sphere):
        """Adiciona um objeto à cena."""
        self.objects.append(obj)

    # Futuramente, podemos adicionar métodos para adicionar luzes,
    # obter o objeto mais próximo que um raio intersecta, etc.