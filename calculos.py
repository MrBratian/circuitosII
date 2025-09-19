import cmath
import math

def mostrar(nombre, z):
    rect = f"{round(z.real,2)}{'+' if z.imag>=0 else ''}{round(z.imag,2)}j"
    mag = abs(z)
    ang = math.degrees(cmath.phase(z))
    polar = f"{round(mag,2)} ∠ {round(ang,2)}°"
    print(f"{nombre} = {rect} = {polar}")

def mostrar_potencia(nombre, S):
    rect = f"{round(S.real,2)}{'+' if S.imag>=0 else ''}{round(S.imag,2)}j VA"
    mag = abs(S)
    ang = math.degrees(cmath.phase(S))
    polar = f"{round(mag,2)} VA ∠ {round(ang,2)}°"
    print(f"Potencia {nombre}: {rect} = {polar}")

def calcular_tensiones_corrientes_potencias(Zs, Vlinea, tipo):
    if tipo == 1:
        Vfase = Vlinea / math.sqrt(3)
        Stot = 0
        Qtot = 0
        for i, Z in enumerate(Zs):
            Ifase = Vfase / Z
            S = Vfase * complex(Ifase).conjugate()
            Q = S.imag
            Stot += S
            Qtot += Q
            print(f"Fase {i+1} (Estrella):")
            print(f"  Tensión de fase = {round(Vfase,2)} V")
            print(f"  Corriente de fase = Corriente de línea = {round(abs(Ifase),2)} A ∠ {round(math.degrees(cmath.phase(Ifase)),2)}°")
            mostrar_potencia(f"Fase {i+1}", S)
            print(f"  Potencia reactiva (Q): {round(Q,2)} var = {round(Q/1000,3)} kVAR")
        print("\nPotencia trifásica total:")
        mostrar_potencia("Trifásica", Stot)
        print(f"Potencia reactiva total (Q): {round(Qtot,2)} var = {round(Qtot/1000,3)} kVAR")
    else:
        Vfase = Vlinea
        Stot = 0
        Qtot = 0
        for i, Z in enumerate(Zs):
            Ifase = Vfase / Z
            Ilinea = abs(Ifase) * math.sqrt(3)
            angI = math.degrees(cmath.phase(Ifase))
            S = Vfase * complex(Ifase).conjugate()
            Q = S.imag
            Stot += S
            Qtot += Q
            print(f"Fase {i+1} (Triángulo):")
            print(f"  Tensión de fase = {round(Vfase,2)} V")
            print(f"  Corriente de fase = {round(abs(Ifase),2)} A ∠ {round(angI,2)}°")
            print(f"  Corriente de línea = {round(Ilinea,2)} A")
            mostrar_potencia(f"Fase {i+1}", S)
            print(f"  Potencia reactiva (Q): {round(Q,2)} var = {round(Q/1000,3)} kVAR")
        print("\nPotencia trifásica total:")
        mostrar_potencia("Trifásica", Stot)
        print(f"Potencia reactiva total (Q): {round(Qtot,2)} var = {round(Qtot/1000,3)} kVAR")
