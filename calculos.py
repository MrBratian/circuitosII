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

def calcular_tensiones_corrientes_potencias(
    Zs, Vlinea, tipo_carga, balanceado=1, tipo_fuente=1, ang_v1=0
):
    print("\n--- Datos de la FUENTE ---")
    # Fases de la fuente
    angulos = [ang_v1, ang_v1 - 120, ang_v1 + 120]
    if tipo_fuente == 1:
        Vfase_fuente = Vlinea / math.sqrt(3)
        print(f"Fuente en estrella (Y):")
        print(f"  Tensión de línea: {round(Vlinea,2)} V")
        print(f"  Tensión de fase: {round(Vfase_fuente,2)} V")
        for i, ang in enumerate(angulos):
            Vfase = cmath.rect(Vfase_fuente, math.radians(ang))
            mostrar(f"Vfase_{i+1}", Vfase)
    else:
        Vfase_fuente = Vlinea
        print(f"Fuente en triángulo (Δ):")
        print(f"  Tensión de línea y fase: {round(Vlinea,2)} V")
        for i, ang in enumerate(angulos):
            Vfase = cmath.rect(Vfase_fuente, math.radians(ang))
            mostrar(f"Vfase_{i+1}", Vfase)
    print("\n--- Tensiones de LÍNEA ---")
    # Tensión de línea entre fases
    for i in range(3):
        v1 = cmath.rect(Vfase_fuente, math.radians(angulos[i]))
        v2 = cmath.rect(Vfase_fuente, math.radians(angulos[(i+1)%3]))
        Vline = v1 - v2
        mostrar(f"Vlinea_{i+1}{(i+2)%3+1}", Vline)
    print("\n--- Datos de las LÍNEAS ---")
    for i, Z in enumerate(Zs):
        Ifase = Vfase_fuente / Z
        if tipo_carga == 1:
            Ilinea = Ifase
        else:
            Ilinea = abs(Ifase) * math.sqrt(3)
        print(f"Línea {i+1}:")
        print(f"  Corriente de línea = {round(abs(Ilinea),2)} A ∠ {round(math.degrees(cmath.phase(Ifase)),2)}°")
    print("\n--- Datos de las CARGAS ---")
    Stot = 0
    Qtot = 0
    for i, Z in enumerate(Zs):
        Ifase = Vfase_fuente / Z
        S = Vfase_fuente * complex(Ifase).conjugate()
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
