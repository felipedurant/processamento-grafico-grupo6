class Material:
    """
    Representa as propriedades fisicas de um material para renderizacao.

    Atributos:
        color (tuple): Cor do material como uma tupla (R, G, B).
        ambient (float): Coeficiente ambiental, que afeta a luminosidade ambiente percebida.
        diffuse (float): Coeficiente lambertiano do material, que afeta a difusao da luz.
        specular (float): Coeficiente especular do material, que afeta o brilho especular.
        shininess (float): Expoente especular (controla o tamanho do brilho)
        reflection (float): O quão espelhado/reflexivo é o material
        transparency (float): O quão transparente é o material
        ior (float): Índice de Refração
        is_checkerboard (bool): Textura procedural, uma textura gerada por código e matemática, em vez de um arquivo de imagem.
    """

    def __init__(self,
                color,
                ambient=0.2,
                diffuse=0.9,
                specular=0.5,
                shininess=32.0,
                reflection=0.2,
                transparency=1.5,
                ior=1.5,
                is_checkerboard: bool = False):
        
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular 
        self.shininess = shininess   
        self.reflection = reflection
        self.transparency = transparency
        self.ior = ior
        self.is_checkerboard = is_checkerboard