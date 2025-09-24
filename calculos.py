import cmath
import math

def mostrar(nombre, z):
    mag = abs(z)
    ang = math.degrees(cmath.phase(z))
    print(f"{nombre}: {mag:.6f} | {ang:.6f}")

def mostrar_potencia(nombre, S):
    print(f"{nombre}: {S.real:.3f}+j{S.imag:.3f}")

def calcular_tensiones_corrientes_potencias(
    Zs, Vlinea, tipo_carga, balanceado=1, tipo_fuente=1, ang_v1=0
):
    print("\n--- DATOS DE LA FUENTE ---")
    angulos = [ang_v1, ang_v1 - 120, ang_v1 + 120]

    # 1. TENSIONES DE FASE Y DE LÍNEA
    if tipo_fuente == 1:  # Fuente estrella
        Vfase_fuente = Vlinea / math.sqrt(3)
        Vfasores_fuente = [cmath.rect(Vfase_fuente, math.radians(a)) for a in angulos]
        Vlineas_fuente = [cmath.rect(Vlinea, math.radians(a)) for a in angulos]
    else:  # Fuente triángulo
        Vfase_fuente = Vlinea
        Vfasores_fuente = [cmath.rect(Vfase_fuente, math.radians(a)) for a in angulos]
        Vlineas_fuente = Vfasores_fuente.copy()

    print("\nTensiones de fase:")
    for i, V in enumerate(Vfasores_fuente):
        mostrar(f"Vfase_{i+1}", V)
    print("\nTensiones de línea:")
    for i, V in enumerate(Vlineas_fuente):
        mostrar(f"Vlinea_{i+1}", V)

    # 2. CORRIENTES DE FASE Y DE LÍNEA
    print("\nCorrientes de fase:")
    Ifases = []
    Vcargas = []
    if tipo_carga == 1:  # Carga estrella
        for i, Z in enumerate(Zs):
            Ifase = Vfasores_fuente[i] / Z
            Ifases.append(Ifase)
            mostrar(f"Ifase_{i+1}", Ifase)
        print("\nCorrientes de línea:")
        for i, Ifase in enumerate(Ifases):
            mostrar(f"Ilinea_{i+1}", Ifase)
        Ilineas = Ifases.copy()
    else:  # Carga triángulo
        # Cada impedancia está entre dos líneas
        # Z1 entre L1-L2, Z2 entre L2-L3, Z3 entre L3-L1
        # V12 = V1 - V2, V23 = V2 - V3, V31 = V3 - V1
        V12 = Vlineas_fuente[0] - Vlineas_fuente[1]
        V23 = Vlineas_fuente[1] - Vlineas_fuente[2]
        V31 = Vlineas_fuente[2] - Vlineas_fuente[0]
        Vcargas = [V12, V23, V31]
        for i, Z in enumerate(Zs):
            Ifase = Vcargas[i] / Z
            Ifases.append(Ifase)
            mostrar(f"Ifase_{i+1}", Ifase)
        print("\nCorrientes de línea:")
        # I_L1 = I_Z1 - I_Z3, I_L2 = I_Z2 - I_Z1, I_L3 = I_Z3 - I_Z2
        Ilinea_1 = Ifases[0] - Ifases[2]
        Ilinea_2 = Ifases[1] - Ifases[0]
        Ilinea_3 = Ifases[2] - Ifases[1]
        Ilineas = [Ilinea_1, Ilinea_2, Ilinea_3]
        for i, Ilinea in enumerate(Ilineas):
            mostrar(f"Ilinea_{i+1}", Ilinea)

    # 3. LECTURAS DE VATÍMETROS (CONEXIÓN ARON)
    print("\nLecturas de vatímetros (conexión Aron):")
    # Vatímetro 1: V12 * I_L1* (conjugada)
    # Vatímetro 2: V32 * I_L3* (conjugada)
    V12 = Vlineas_fuente[0] - Vlineas_fuente[1]
    V32 = Vlineas_fuente[2] - Vlineas_fuente[1]
    W1 = V12 * Ilineas[0].conjugate()
    W2 = V32 * Ilineas[2].conjugate()
    print(f"Vatímetro 1 (L1-L2): {W1.real:.2f} W")
    print(f"Vatímetro 2 (L3-L2): {W2.real:.2f} W")

    # 4. POTENCIAS
    print("\nPotencia compleja por fase:")
    potencias = []
    Stot = 0
    for i in range(3):
        if tipo_carga == 1:
            S = Vfasores_fuente[i] * Ifases[i].conjugate()
        else:
            S = Vcargas[i] * Ifases[i].conjugate()
        potencias.append(S)
        mostrar_potencia(f"Fase {i+1}", S)
        Stot += S
    print("\nPotencia compleja trifásica:")
    mostrar_potencia("Total", Stot)

    return Vfasores_fuente, Vlineas_fuente, Ifases, Ilineas, potencias + [Stot]
