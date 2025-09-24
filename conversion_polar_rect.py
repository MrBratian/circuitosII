import math
import cmath

def convertir_polar_rectangular():
    print("Seleccione conversión:")
    print("1) Polar a Rectangular")
    print("2) Rectangular a Polar")
    op = int(input("> "))
    if op == 1:
        mag = float(input("Magnitud: "))
        ang = float(input("Ángulo (grados): "))
        z = cmath.rect(mag, math.radians(ang))
        print(f"Rectangular: {z.real:.4f} {'+' if z.imag>=0 else '-'} {abs(z.imag):.4f}j")
    else:
        real = float(input("Parte real: "))
        imag = float(input("Parte imaginaria: "))
        z = complex(real, imag)
        mag = abs(z)
        ang = math.degrees(cmath.phase(z))
        print(f"Polar: {mag:.4f} ∠ {ang:.2f}°")

if __name__ == "__main__":
    convertir_polar_rectangular()