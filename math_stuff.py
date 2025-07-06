#import numpy as np # Para teste

def factorial(n):
    """Função recursiva que faz o calculo do fatorial de um número especificado."""
    if n == 0:
        return 1
    else:
        return  n * factorial(n-1)

def degree_to_rad(degree : float):
    """Converte um valor de graus para radianos."""
    return degree * 3.1415926535897932384626433 / 180

# 
def sin(rad : float, n : int = 12):
    """Calcula o seno, utilisando uma série de Taylor que obtem um valor aproximado ao da função do seno."""
    seno = 0
    for i in range(n):
        termo = (-1)**i * (rad**(2*i + 1)) / factorial(2*i + 1)
        seno += termo
    return seno

def cos(rad : float, n : int = 12):
    """Calcula o cosseno, utilisando uma série de Taylor que obtem um valor aproximado ao da função do cosseno."""
    cosseno = 0
    for i in range(n):
        termo = (-1)**i * (rad**(2*i)) / factorial(2*i)
        cosseno += termo
    return cosseno