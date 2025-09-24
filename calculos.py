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

def calcular_tensiones_corrientes_potencias(Zs, Vlinea, tipo, balanceado=1):
    print("\n--- Datos de la FUENTE ---")
    if tipo == 1:
        Vfase = Vlinea / math.sqrt(3)
        print(f"Tensión de línea: {round(Vlinea,2)} V")
        print(f"Tensión de fase: {round(Vfase,2)} V")
    else:
        Vfase = Vlinea
        print(f"Tensión de línea y fase: {round(Vlinea,2)} V")
    print("\n--- Datos de las LÍNEAS ---")
    for i, Z in enumerate(Zs):
        Ifase = Vfase / Z
        if tipo == 1:
            Ilinea = Ifase
        else:
            Ilinea = abs(Ifase) * math.sqrt(3)
        print(f"Línea {i+1}:")
        print(f"  Corriente de línea = {round(abs(Ilinea),2)} A ∠ {round(math.degrees(cmath.phase(Ifase)),2)}°")
    print("\n--- Datos de las CARGAS ---")
    Stot = 0
    Qtot = 0
    for i, Z in enumerate(Zs):
        Ifase = Vfase / Z
        S = Vfase * complex(Ifase).conjugate()
        Q = S.imag
        Stot += S
        Qtot += Q
        print(f"Carga {i+1}:")
        print(f"  Corriente de fase = {round(abs(Ifase),2)} A ∠ {round(math.degrees(cmath.phase(Ifase)),2)}°")
        mostrar_potencia(f"Carga {i+1}", S)
        print(f"  Potencia reactiva (Q): {round(Q,2)} var = {round(Q/1000,3)} kVAR")
    print("\nPotencia trifásica total:")
    mostrar_potencia("Trifásica", Stot)
    print(f"Potencia reactiva total (Q): {round(Qtot,2)} var = {round(Qtot/1000,3)} kVAR")
    if balanceado == 1:
        print("\nEl circuito es balanceado: todas las fases tienen los mismos valores.")
    else:
        print("\nEl circuito es desbalanceado: los valores pueden variar entre fases.")
