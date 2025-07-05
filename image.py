# Dentro de image.py
from PIL import Image as PillowImage

class Image:
    """
    Representa uma imagem em memória, que pode ser salva em um arquivo.
    Usa a biblioteca Pillow para manipulação e salvamento.
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Cria uma imagem preta em memória usando a biblioteca Pillow
        self.image = PillowImage.new("RGB", (width, height), "black")
        # Prepara um objeto para permitir a escrita de pixels
        self.pixels = self.image.load()

    def set_pixel(self, x: int, y: int, color: tuple):
        """
        Define a cor de um pixel específico.

        Args:
            x (int): Coordenada horizontal do pixel.
            y (int): Coordenada vertical do pixel.
            color (tuple): Tupla (R, G, B) com valores de 0 a 255.
        """
        # A biblioteca Pillow espera tuplas de inteiros para as cores
        int_color = (int(color[0]), int(color[1]), int(color[2]))
        
        # O acesso aos pixels é feito como [x, y]
        # A origem (0,0) para Pillow é no canto superior esquerdo, então invertemos o Y
        self.pixels[x, self.height - 1 - y] = int_color

    def save(self, path: str):
        """
        Salva a imagem em um arquivo. O formato é determinado pela extensão.

        Exemplos de path: "minha_imagem.png", "cena.jpg", "output.bmp"
        """
        self.image.save(path)
        print(f"Imagem salva em: {path}")