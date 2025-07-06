from vector import Vector
from point import Point
import math_stuff as ms

class Matrix:
    def __init__(self, matrix_values : list):
        self.values = matrix_values
        self.n_linhas= len(self.values)
        self.n_colunas= len(self.values[0])

    def __str__(self):
        """Função que cria uma representação da matriz em string."""
        values_string = ""
        for l in range(self.n_linhas):
            values_string += "["
            for c  in range(self.n_colunas):
                if c == 0:
                    values_string += f"{self.values[l][c]:>10.5f}"
                else:
                    values_string += f", {self.values[l][c]:>15.5f}"
            values_string += "]\n"
        return values_string
    
    def set_value(self, line : int, column : int, value : float):
        """
        Função que muda um valor especifico da matriz.

        Args:
        line (int): Número da linha da matriz em que o valor está, começa a partir do indice 1.
        column (int): Número da coluna da matriz em que o valor está, comaça a partir do inice 1.
        value (float): Valor que será colocado na posição especificada. 
        """
        self.values[line-1][column-1] = value

    def copy_values(self):
        """
        Função que cria uma copia dos valores da matriz.
        
        Return:
        Copia dos valores.
        """
        copy = []
        for l in range(self.n_linhas):
            copy.append([])
            for c in range(self.n_colunas):
                copy[l].append(self.values[l][c])
        return copy

    def inverse(self):
        """
        Função que faz a calcula a inversa da matriz utilizando a eliminação de Gauss-Jordan.
        
        Return:
        Matriz inversa encontrada.
        """
        if self.n_linhas == self.n_colunas:
            # Cria copia para não substituir os valores originais.
            n = self.n_colunas
            matriz = self.copy_values()

            # Concatena a matriz com a matriz identidade.
            matriz_identidade = self.create_identity_matrix(n).copy_values()
            matriz_concat = []
            for i in range(n):
                matriz_concat.append(matriz[i] + matriz_identidade[i])
            
            # Repete os passos a seguir para todas as colunas da matriz. 
            for coluna in range(n):
                # Encontra o indice da linha do maior valor da coluna atual.
                maior_index = 0
                maior = 0
                for i in range(coluna, n):
                    valor = matriz_concat[i][coluna]
                    if maior < abs(valor):
                        maior = valor
                        maior_index = i
                # Troca de lugar a linha com o mesmo indice da coluna atual e a linha com o maior valor da coluna.
                matriz_concat[coluna], matriz_concat[maior_index] = matriz_concat[maior_index], matriz_concat[coluna]

                # Transforma linha para que elemento da diagonal vire um.
                escalar = matriz_concat[coluna][coluna]
                matriz_concat[coluna] = [elemento / escalar for elemento in matriz_concat[coluna]]

                # Para todas as linhas diferentes da coluna atual, vai tornar os elementos da coluna que não estão na diagonal
                # principal iguais a 0, faz isso multiplicando os valores da linha que tem o mesmo indice da coluna atual 
                # pelos valores dos elementos das outras linhas, que estão na mesma coluna, e depois subtraindo nessas linhas.
                for linha in range(n):
                    if linha != coluna:
                        escalar = matriz_concat[linha][coluna]
                        matriz_concat[linha] = [elemento - (escalar * matriz_concat[coluna][i])
                                                for i, elemento in enumerate(matriz_concat[linha])]
            
            # Retira a matriz invertida da matriz concatenada.
            matriz_invertida = []
            for i in range(n):
                matriz_invertida.append(matriz_concat[i][n:])
            return Matrix(matriz_invertida)
        else:
            return None

    def dot_product(self, other):
        """
        Função que calcula o produto escalar entre a matriz e outras coisas como: pontos, vetores e outras matrizes.
        Para isso essa coisa é temporariamente convertida em uma matriz e depois das contas seu resultado é convertido
        de volta.

        Args:
        other: Coisa com a qual será calculado o produto escalar, pode ser um Vector, um Point ou uma Matrix.

        Return:
        O retorno tem a mesma forma da coisa que foi recebida como parametro, então se foi recebido um Vetor
        o resultado estará na form de um vetor, se foi recebido um Ponto o resultado será um ponto e se foi
        recebido uma matriz o resultado será outra matriz.
        """
        # Com Vector:
        if isinstance(other, (Vector)):
            other_matrix = self.to_matrix(other)
            result = self.dot_product_matrix(self, other_matrix)
            if result != None:
                result = self.matrix_to(result, Vector)
            return result
        # Com Point:
        elif isinstance(other, (Point)):
            other_matrix = self.to_matrix(other)
            result = self.dot_product_matrix(self, other_matrix)
            if result != None:
                result = self.matrix_to(result, Point)
            return result
        # Com Matrix:
        elif isinstance(other, Matrix):
            other_matrix = other
            result = self.dot_product_matrix(self, other_matrix)
            return result
        else:
            return None
    
    @staticmethod
    def dot_product_matrix(matrix1, matrix2):
        """Faz o produto escalar entre duas matrizes."""
        if matrix2.n_linhas== matrix1.n_colunas:
            result = []
            for l in range(matrix1.n_linhas):
                result.append([])
                for c in range(matrix2.n_colunas):
                    position_value = 0
                    for i in range(matrix2.n_linhas):
                        position_value += matrix1.values[l][i] * matrix2.values[i][c]
                    result[l].append(position_value)
            return Matrix(result)
        else:
            return None

    @staticmethod
    def to_matrix(thing):
        """Converte Vector e Point para Matrix."""
        if isinstance(thing, (Vector, Point)):
            values = [[thing.x], [thing.y], [thing.z], [1]]
            return Matrix(values)
        else:
            return None

    @staticmethod
    def matrix_to(matrix, to_type):
        """Converte uma Matrix para um ponto ou vetor."""
        return to_type(matrix.values[0][0], matrix.values[1][0], matrix.values[2][0])

    @staticmethod
    def create_identity_matrix(size : int):
        """Função que cria e retorna a matriz identidade do tamanho especificado."""
        ident = []
        for i in range(size):
            ident.append([])
            for j in range(size):
                if i == j:
                    ident[i].append(1)
                else:
                    ident[i].append(0)
        return Matrix(ident)

    @staticmethod
    def create_defaut_matrix():
        """Função que cria uma matriz de transformação padrão (que não faz nada)."""
        m = [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]]
        return m

    @staticmethod
    def create_move_matrix(move_direction : Vector):
        """Cria uma matriz de transformação de movimento, de acordo com o vetor que indica a direção do movimento."""
        m = [[1, 0, 0, move_direction.x],
             [0, 1, 0, move_direction.y],
             [0, 0, 1, move_direction.z],
             [0, 0, 0, 1               ]]
        return Matrix(m)

    @staticmethod
    def create_rotation_matrix(degree : float, axis : int = 0):
        """
        Função que cria uma matriz de transformação de rotação, o padrão da rotação é o sentido anti-horario.
        Obs: Faz apenas a parte da rotação, não faz a parte do deslocamento para a origem.

        Args:
        degree (float): quantidade de graus que será rotacionado.
        axis (0, 1 ou 2): Eixo que ficará fixo durante a na rotação, 0 = x, 1 = y e 2 = z.

        Return:
        Matrix que faz a operação de rotação. 
        """
        if axis == 0 or axis == 1 or axis == 2:
            angle = ms.degree_to_rad(degree)
            if axis == 0:
                m = [[1, 0            ,  0            , 0],
                     [0, ms.cos(angle), -ms.sin(angle), 0],
                     [0, ms.sin(angle),  ms.cos(angle), 0],
                     [0, 0            ,  0            , 1]]
            elif axis == 1:
                m = [[ ms.cos(angle), 0, ms.sin(angle), 0],
                     [ 0            , 1, 0            , 0],
                     [-ms.sin(angle), 0, ms.cos(angle), 0],
                     [ 0            , 0, 0            , 1]]
            elif axis == 2:
                m = [[ms.cos(angle), -ms.sin(angle), 0, 0],
                     [ms.sin(angle),  ms.cos(angle), 0, 0],
                     [0            ,  0            , 1, 0],
                     [0            ,  0            , 0, 1]]
            return Matrix(m)
        else:
            return Matrix.create_defaut_matrix()

    @staticmethod
    def create_scale_matrix(scale_vector : Vector):
        """Função que faz uma matriz de transformação de escala, de acordo com o vetor recebido."""
        m = [[scale_vector.x,              0,              0, 0],
             [             0, scale_vector.y,              0, 0],
             [             0,              0, scale_vector.z, 0],
             [             0,              0,              0, 1]]
        return Matrix(m)
    pass