import math
import cmath
from conversiones import estrella_a_triangulo, triangulo_a_estrella
from calculos import mostrar, mostrar_potencia, calcular_tensiones_corrientes_potencias

def leer_impedancia(nombre, formato):
    if formato == 1: # Rectangular
        r = float(input(f"Parte real de {nombre}: "))
        i = float(input(f"Parte imaginaria de {nombre}: "))
        return complex(r, i)
    else: # Polar
        mag = float(input(f"Magnitud de {nombre}: "))
        ang = float(input(f"Ángulo (grados) de {nombre}: "))
        rad = math.radians(ang)
        return cmath.rect(mag, rad)

def main():
    print("Seleccione una opción:")
    print("1) Estrella a Triángulo")
    print("2) Triángulo a Estrella")
    print("3) Calcular tensiones, corrientes y potencias (incluye lectura de varímetro)")
    print("4) Conversión entre polar y rectangular")
    op = int(input("> "))
    if op == 1:
        print("\n¿El circuito es balanceado?")
        print("1) Sí")
        print("2) No")
        balanceado = int(input("> "))
        print("\nFormato de entrada:")
        print("1) Rectangular (real, imag)")
        print("2) Polar (magnitud, ángulo en grados)")
        formato = int(input("> "))
        if balanceado == 1:
            Za = leer_impedancia("Za", formato)
            Zb = Za
            Zc = Za
        else:
            Za = leer_impedancia("Za", formato)
            Zb = leer_impedancia("Zb", formato)
            Zc = leer_impedancia("Zc", formato)
        Z1, Z2, Z3 = estrella_a_triangulo(Za, Zb, Zc)
        print("\nResultados:")
        mostrar("Z1", Z1)
        mostrar("Z2", Z2)
        mostrar("Z3", Z3)
    elif op == 2:
        print("\n¿El circuito es balanceado?")
        print("1) Sí")
        print("2) No")
        balanceado = int(input("> "))
        print("\nFormato de entrada:")
        print("1) Rectangular (real, imag)")
        print("2) Polar (magnitud, ángulo en grados)")
        formato = int(input("> "))
        if balanceado == 1:
            Z1 = leer_impedancia("Z1", formato)
            Z2 = Z1
            Z3 = Z1
        else:
            Z1 = leer_impedancia("Z1", formato)
            Z2 = leer_impedancia("Z2", formato)
            Z3 = leer_impedancia("Z3", formato)
        Za, Zb, Zc = triangulo_a_estrella(Z1, Z2, Z3)
        print("\nResultados:")
        mostrar("Za", Za)
        mostrar("Zb", Zb)
        mostrar("Zc", Zc)
    elif op == 3:
        print("\nTipo de conexión de la fuente:")
        print("1) Estrella (Y)")
        print("2) Triángulo (Δ)")
        tipo_fuente = int(input("> "))
        print("\nFormato de entrada de la tensión de línea:")
        print("1) Rectangular (real, imag)")
        print("2) Polar (magnitud, ángulo en grados)")
        formato_tension = int(input("> "))
        if formato_tension == 1:
            real = float(input("Parte real de la tensión de línea: "))
            imag = float(input("Parte imaginaria de la tensión de línea: "))
            Vlinea = complex(real, imag)
            ang_v1 = math.degrees(cmath.phase(Vlinea))
            Vlinea_mag = abs(Vlinea)
        else:
            Vlinea_mag = float(input("Magnitud de la tensión de línea: "))
            ang_v1 = float(input("Ángulo de la primera fase de la fuente (en grados): "))
            Vlinea = cmath.rect(Vlinea_mag, math.radians(ang_v1))
        print("\nTipo de conexión de la carga:")
        print("1) Estrella (Y)")
        print("2) Triángulo (Δ)")
        tipo_carga = int(input("> "))
        print("\n¿El circuito es balanceado?")
        print("1) Sí")
        print("2) No")
        balanceado = int(input("> "))
        print("\nFormato de entrada de impedancias:")
        print("1) Rectangular (real, imag)")
        print("2) Polar (magnitud, ángulo en grados)")
        formato = int(input("> "))
        if tipo_carga == 1:
            if balanceado == 1:
                print("\nIngrese la impedancia de fase (Za):")
                Za = leer_impedancia("Za", formato)
                Zs = [Za, Za, Za]
            else:
                print("\nIngrese las impedancias de fase (Za, Zb, Zc):")
                Za = leer_impedancia("Za", formato)
                Zb = leer_impedancia("Zb", formato)
                Zc = leer_impedancia("Zc", formato)
                Zs = [Za, Zb, Zc]
        else:
            if balanceado == 1:
                print("\nIngrese la impedancia de triángulo (Z):")
                Z1 = leer_impedancia("Z", formato)
                Zs = [Z1, Z1, Z1]
            else:
                print("\nIngrese las impedancias de triángulo (Z1, Z2, Z3):")
                Z1 = leer_impedancia("Z1", formato)
                Z2 = leer_impedancia("Z2", formato)
                Z3 = leer_impedancia("Z3", formato)
                Zs = [Z1, Z2, Z3]
        print("\nResultados:")
        calcular_tensiones_corrientes_potencias(
            Zs, Vlinea_mag, tipo_carga, balanceado, tipo_fuente, ang_v1
        )
    elif op == 4:
        from conversion_polar_rect import convertir_polar_rectangular
        convertir_polar_rectangular()

if __name__ == "__main__":
    main()
