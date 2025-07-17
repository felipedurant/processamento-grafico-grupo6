# Em matrix.py

import math
from typing import overload, Union

# Bloco para dicas de tipo que evita importação circular
if False:
    from point import Point
    from vector import Vector
    from ray import Ray

class Matrix4:
    """
    Representa uma matriz 4x4 utilizada para transformações afins em 3D.
    """
    def __init__(self, values=None):
        if values is None:
            self.values = [[(1 if i == j else 0) for j in range(4)] for i in range(4)]
        else:
            self.values = values

    def __str__(self):
        return '\n'.join(['[' + ', '.join([f'{v:8.3f}' for v in row]) + ']' for row in self.values])



    @overload
    def __mul__(self, other: 'Matrix4') -> 'Matrix4': ...

    @overload
    def __mul__(self, other: 'Point') -> 'Point': ...

    @overload
    def __mul__(self, other: 'Vector') -> 'Vector': ...


    def __mul__(self, other: Union['Matrix4', 'Point', 'Vector']):
        from point import Point
        from vector import Vector

        if isinstance(other, Matrix4):
            new_values = [[0] * 4 for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        new_values[i][j] += self.values[i][k] * other.values[k][j]
            return Matrix4(new_values)

        if isinstance(other, (Point, Vector)):
            is_point = isinstance(other, Point)
            coords = [other.x, other.y, other.z, 1.0 if is_point else 0.0]
            new_coords = [0.0] * 4

            for i in range(4):
                for j in range(4):
                    new_coords[i] += self.values[i][j] * coords[j]
            
            if is_point:
                w = new_coords[3]
                if w != 1.0 and w != 0.0:
                    return Point(new_coords[0] / w, new_coords[1] / w, new_coords[2] / w)
                return Point(new_coords[0], new_coords[1], new_coords[2])
            else:
                return Vector(new_coords[0], new_coords[1], new_coords[2])
        
        return NotImplemented


    def transpose(self) -> 'Matrix4':
        """Retorna a transposta desta matriz (troca linhas por colunas)."""
        return Matrix4([[self.values[j][i] for j in range(4)] for i in range(4)])

    def inverse(self) -> 'Matrix4':
        """Calcula e retorna a matriz inversa completa."""
        m = [v for row in self.values for v in row]
        inv = [0] * 16
        inv[0]  =  m[5]*m[10]*m[15] - m[5]*m[11]*m[14] - m[9]*m[6]*m[15] + m[9]*m[7]*m[14] + m[13]*m[6]*m[11] - m[13]*m[7]*m[10]
        inv[4]  = -m[4]*m[10]*m[15] + m[4]*m[11]*m[14] + m[8]*m[6]*m[15] - m[8]*m[7]*m[14] - m[12]*m[6]*m[11] + m[12]*m[7]*m[10]
        inv[8]  =  m[4]*m[9]*m[15] - m[4]*m[11]*m[13] - m[8]*m[5]*m[15] + m[8]*m[7]*m[13] + m[12]*m[5]*m[11] - m[12]*m[7]*m[9]
        inv[12] = -m[4]*m[9]*m[14] + m[4]*m[10]*m[13] + m[8]*m[5]*m[14] - m[8]*m[6]*m[13] - m[12]*m[5]*m[10] + m[12]*m[6]*m[9]
        inv[1]  = -m[1]*m[10]*m[15] + m[1]*m[11]*m[14] + m[9]*m[2]*m[15] - m[9]*m[3]*m[14] - m[13]*m[2]*m[11] + m[13]*m[3]*m[10]
        inv[5]  =  m[0]*m[10]*m[15] - m[0]*m[11]*m[14] - m[8]*m[2]*m[15] + m[8]*m[3]*m[14] + m[12]*m[2]*m[11] - m[12]*m[3]*m[10]
        inv[9]  = -m[0]*m[9]*m[15] + m[0]*m[11]*m[13] + m[8]*m[1]*m[15] - m[8]*m[3]*m[13] - m[12]*m[1]*m[11] + m[12]*m[3]*m[9]
        inv[13] =  m[0]*m[9]*m[14] - m[0]*m[10]*m[13] - m[8]*m[1]*m[14] + m[8]*m[2]*m[13] + m[12]*m[1]*m[10] - m[12]*m[2]*m[9]
        inv[2]  =  m[1]*m[6]*m[15] - m[1]*m[7]*m[14] - m[5]*m[2]*m[15] + m[5]*m[3]*m[14] + m[13]*m[2]*m[7] - m[13]*m[3]*m[6]
        inv[6]  = -m[0]*m[6]*m[15] + m[0]*m[7]*m[14] + m[4]*m[2]*m[15] - m[4]*m[3]*m[14] - m[12]*m[2]*m[7] + m[12]*m[3]*m[6]
        inv[10] =  m[0]*m[5]*m[15] - m[0]*m[7]*m[13] - m[4]*m[1]*m[15] + m[4]*m[3]*m[13] + m[12]*m[1]*m[7] - m[12]*m[3]*m[5]
        inv[14] = -m[0]*m[5]*m[14] + m[0]*m[6]*m[13] + m[4]*m[1]*m[14] - m[4]*m[2]*m[13] - m[12]*m[1]*m[6] + m[12]*m[2]*m[5]
        inv[3]  = -m[1]*m[6]*m[11] + m[1]*m[7]*m[10] + m[5]*m[2]*m[11] - m[5]*m[3]*m[10] - m[9]*m[2]*m[7] + m[9]*m[3]*m[6]
        inv[7]  =  m[0]*m[6]*m[11] - m[0]*m[7]*m[10] - m[4]*m[2]*m[11] + m[4]*m[3]*m[10] + m[8]*m[2]*m[7] - m[8]*m[3]*m[6]
        inv[11] = -m[0]*m[5]*m[11] + m[0]*m[7]*m[9] + m[4]*m[1]*m[11] - m[4]*m[3]*m[9] - m[8]*m[1]*m[7] + m[8]*m[3]*m[5]
        inv[15] =  m[0]*m[5]*m[10] - m[0]*m[6]*m[9] - m[4]*m[1]*m[10] + m[4]*m[2]*m[9] + m[8]*m[1]*m[6] - m[8]*m[2]*m[5]

        det = m[0]*inv[0] + m[1]*inv[4] + m[2]*inv[8] + m[3]*inv[12]
        if det == 0:
            raise ValueError("A matriz não tem inversa (determinante é zero).")
        
        det = 1.0 / det
        inv_matrix = [[inv[i*4+j] * det for j in range(4)] for i in range(4)]
        return Matrix4(inv_matrix)

    @staticmethod
    def identity():
        return Matrix4()

    @staticmethod
    def translation(x, y, z):
        mat = Matrix4.identity()
        mat.values[0][3] = x
        mat.values[1][3] = y
        mat.values[2][3] = z
        return mat

    @staticmethod
    def scaling(x, y, z):
        mat = Matrix4.identity()
        mat.values[0][0] = x
        mat.values[1][1] = y
        mat.values[2][2] = z
        return mat

    @staticmethod
    def rotation_x(angle_degrees):
        angle_rad = math.radians(angle_degrees)
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        mat = Matrix4.identity()
        mat.values[1][1] = c
        mat.values[1][2] = -s
        mat.values[2][1] = s
        mat.values[2][2] = c
        return mat

    @staticmethod
    def rotation_y(angle_degrees):
        angle_rad = math.radians(angle_degrees)
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        mat = Matrix4.identity()
        mat.values[0][0] = c
        mat.values[0][2] = s
        mat.values[2][0] = -s
        mat.values[2][2] = c
        return mat

    @staticmethod
    def rotation_z(angle_degrees):
        angle_rad = math.radians(angle_degrees)
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        mat = Matrix4.identity()
        mat.values[0][0] = c
        mat.values[0][1] = -s
        mat.values[1][0] = s
        mat.values[1][1] = c
        return mat