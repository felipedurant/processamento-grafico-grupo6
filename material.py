from typing import Optional

class Material:
    """
    Representa as propriedades fisicas de um material para renderizacao.

    Atributos:
        color (tuple): Cor do material como uma tupla (R, G, B).
        ambient (RGB): Coeficiente ambiental, que afeta a luminosidade ambiente percebida.
        diffuse (RGB): Coeficiente lambertiano do material, que afeta a difusao da luz.
        specular (RGB): Coeficiente especular do material, que afeta o brilho especular.
        shininess (float): Expoente especular (controla o tamanho do brilho)
        reflection (float): O quão espelhado/reflexivo é o material
        transparency (float): O quão transparente é o material
        ior (float): Índice de Refração
        is_checkerboard (bool): Textura procedural, uma textura gerada por código e matemática, em vez de um arquivo de imagem.
    """

    def __init__(self,
                #color,
                ambient: Optional[tuple] = None,
                diffuse: tuple = (255, 255, 255),
                specular: tuple = (255, 255, 255),
                shininess: float = 32.0,
                reflection: float = 0.0,
                transparency: float = 0.0,
                ior: float = 1.0,
                is_checkerboard: bool = False):
        
        #self.color = color
        self.diffuse = diffuse
        # Se ambient não for fornecido, ele será uma fração de diffuse.
        self.ambient = ambient if ambient is not None else (diffuse[0] * 0.1, diffuse[1] * 0.1, diffuse[2] * 0.1)
        self.specular = specular 
        self.shininess = shininess   
        self.reflection = reflection
        self.transparency = transparency
        self.ior = ior
        self.is_checkerboard = is_checkerboard