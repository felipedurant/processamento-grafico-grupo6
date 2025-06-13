class Material:
    """
    Representa as propriedades fisicas de um material para renderizacao.

    Atributos:
        color (tuple): Cor do material como uma tupla (R, G, B).
        specular (float): Coeficiente especular do material, que afeta o brilho especular.
        lambert (float): Coeficiente lambertiano do material, que afeta a difusao da luz.
        ambient (float): Coeficiente ambiental, que afeta a luminosidade ambiente percebida.
        material_type (str): Tipo do material (por exemplo, "DIFFUSE").
        kr (float): indice de refracao do material.
        kt (float): Componente transmissiva do material, que afeta a transparencia.
    """

    def __init__(self, color, specular=0.5, lambert=1, ambient=0.2, material_type="DIFFUSE", kr=1.5, kt=0.5):
        self.color = color
        self.specular = specular 
        self.lambert = lambert  
        self.ambient = ambient  
        self.material_type = material_type 
        self.kr = kr  
        self.kt = kt  


### Classe "Mesh"
 ## - Propósito: Representa uma coleção de vértices, arestas e faces que define a forma de um objeto 3D.
  ##- Funções Comuns: Manipulação e renderização de malhas, transformações geométricas.
