import cmath
import math

def estrella_a_triangulo(Za, Zb, Zc, balanceado=False):
    if balanceado:
        return 3*Za, 3*Za, 3*Za
    num = Za*Zb + Zb*Zc + Zc*Za
    return num/Zc, num/Za, num/Zb

def triangulo_a_estrella(Z1, Z2, Z3, balanceado=False):
    if balanceado:
        return Z1/3, Z1/3, Z1/3
    s = Z1 + Z2 + Z3
    return (Z1*Z3)/s, (Z1*Z2)/s, (Z2*Z3)/s
