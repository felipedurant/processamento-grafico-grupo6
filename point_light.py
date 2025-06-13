class Light:
    """
    Representa uma fonte de luz em uma cena de renderizacao.

    Atributos:
        pos (Vector): A posicao da fonte de luz.
        color (tuple): A cor da luz, representada como uma tupla (R, G, B).
    """

    def __init__(self, pos, color):
        """
        Inicializa uma instancia da fonte de luz com uma posicao e cor especificadas.

        Args:
            pos (Vector): A posicao da fonte de luz.
            color (tuple): A cor da luz.
        """
        self.pos = pos
        self.color = color

    def get_source(self):
        """
        Retorna a posicao da fonte de luz.

        Returns:
            Vector: A posicao da fonte de luz.
        """
        return self.pos


### Classe "PointLight"
##  - Propósito: Representa uma fonte de luz pontual, emitindo luz em todas as direções a partir de um ponto específico.
##  - Funções Comuns: Definição de intensidade e posição da luz, cálculos de iluminação.
