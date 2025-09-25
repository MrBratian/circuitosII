import math
import cmath
from calculos import calcular_tensiones_corrientes_potencias


def leer_impedancia(nombre, formato):
    if formato == 1:  # Rectangular
        r = float(input(f"Parte real de {nombre}: "))
        i = float(input(f"Parte imaginaria de {nombre}: "))
        return complex(r, i)
    else:  # Polar
        mag = float(input(f"Magnitud de {nombre}: "))
        ang = float(input(f"Ángulo (grados) de {nombre}: "))
        return cmath.rect(mag, math.radians(ang))


def _mag_ang_str(z: complex) -> str:
    return f"{abs(z):.6f} | {math.degrees(cmath.phase(z)):.6f}"


def _S_str(S: complex) -> str:
    return f"{S.real:.1f}+j{S.imag:.1f}"


def imprimir_resultados_ordenados(resultado: dict, tipo_carga: str, hilos: int):
    # Extraer con tolerancia
    Vfase_fuente = resultado.get("Vfase_fuente", [])
    Vlinea_fuente = resultado.get("Vlinea_fuente", [])
    Vfase_carga = resultado.get("Vfase_carga") or []
    Vramas_delta = resultado.get("Vramas_delta") or []

    # Decide qué tensiones de fase mostrar (preferir tensiones en carga)
    Vfase_para_mostrar = Vfase_carga if Vfase_carga else Vfase_fuente

    # Tensiones de línea a mostrar: para delta o cuando Vlinea_fuente está disponible,
    # usamos Vlinea_fuente; si no, calculamos diferencias apropiadas.
    Vlineas_display = []
    if Vlinea_fuente:
        Vlineas_display = Vlinea_fuente
    elif Vfase_para_mostrar and len(Vfase_para_mostrar) == 3:
        Vlineas_display = [
            Vfase_para_mostrar[0] - Vfase_para_mostrar[1],
            Vfase_para_mostrar[1] - Vfase_para_mostrar[2],
            Vfase_para_mostrar[2] - Vfase_para_mostrar[0]
        ]

    Ifases = resultado.get("Ifase") or resultado.get("Iramas_delta") or []
    Ilineas = resultado.get("Ilinea") or []
    pot_fases = resultado.get("S_fase") or resultado.get("S_rama") or []
    S_total = resultado.get("S_total")

    print("\nTensiones de fase:")
    if Vfase_para_mostrar:
        for i, V in enumerate(Vfase_para_mostrar, start=1):
            print(f"{i}) {_mag_ang_str(V)}")

    print("\nTensiones de línea:")
    if Vlineas_display:
        for i, V in enumerate(Vlineas_display, start=1):
            print(f"{i}) {_mag_ang_str(V)}")

    print("\nCorrientes de fase:")
    if Ifases:
        for i, I in enumerate(Ifases, start=1):
            print(f"{i}) {_mag_ang_str(I)}")

    print("\nCorrientes de línea:")
    if Ilineas:
        for i, I in enumerate(Ilineas, start=1):
            print(f"{i}) {_mag_ang_str(I)}")

    # Si es Y y hilos == 4 mostrar In explícito
    if tipo_carga.upper() == "Y" and hilos == 4:
        if Ifases:
            In = -sum(Ifases)
            print(f"{len(Ilineas)+1}) {_mag_ang_str(In)}")

    print("\nPotencia compleja por fase:")
    if pot_fases:
        for i, S in enumerate(pot_fases, start=1):
            print(f"{i}) {_S_str(S)}")

    print("\nPotencia compleja trifásica:")
    if S_total is not None:
        print(f"1) {_S_str(S_total)}")

    # Corriente de neutro (solo Y)
    if tipo_carga.upper() == "Y":
        if Ifases:
            In = -sum(Ifases)
            print("\nCorriente de Neutro. INn:")
            print(f"1) {_mag_ang_str(In)}")

    # Corrimiento de neutro (solo Y-3hilos desbalanceado o Y-3hilos balanceado con Δ fuente)
    if tipo_carga.upper() == "Y" and hilos == 3:
        VnN = resultado.get("VnN")
        VNn = resultado.get("VNn")
        if VnN is not None:
            print("\nCorrimiento de Neutro. VnN:")
            print(f"1) {_mag_ang_str(VnN)}")
        if VNn is not None:
            print("\nCorrimiento de Neutro. VNn:")
            print(f"1) {_mag_ang_str(VNn)}")

def main():
    print("CÁLCULO DE CIRCUITOS TRIFÁSICOS")
    print("--------------------------------")
    print("Este programa calcula tensiones, corrientes y potencias en circuitos trifásicos.")
    print("--------------------------------")
    print("\nIniciando cálculo de circuito...\n")

    # Tipo de conexión de la fuente
    print("Tipo de conexión de la fuente:")
    print("1) Estrella (Y)")
    print("2) Triángulo (Δ)")
    tipo_fuente_input = int(input("> "))
    tipo_fuente = "Y" if tipo_fuente_input == 1 else "D"

    # Convención automática: Y -> se ingresa Vfase; Δ -> se ingresa Vlinea
    if tipo_fuente == "Y":
        print("\n(Convención) Fuente ESTRELLA (Y): se asumirá que ingresas Vfase (fase-a-neutro).")
        entrada_prompt = "Magnitud de la tensión de fase (Vfase, en V): "
    else:
        print("\n(Convención) Fuente TRIÁNGULO (Δ): se asumirá que ingresas Vlínea (línea-a-línea).")
        entrada_prompt = "Magnitud de la tensión de línea (Vlinea, en V): "

    entrada_mag = float(input(entrada_prompt))
    ang_v1 = float(input("Ángulo de la primera fase de la fuente (en grados): "))

    if tipo_fuente == "Y":
        Vlinea_mag = entrada_mag * math.sqrt(3)
    else:
        Vlinea_mag = entrada_mag

    # Tipo de conexión de la carga
    print("\nTipo de conexión de la carga:")
    print("1) Estrella (Y)")
    print("2) Triángulo (Δ)")
    tipo_carga_input = int(input("> "))
    tipo_carga = "Y" if tipo_carga_input == 1 else "D"

    # Balanceado?
    print("\n¿El circuito es balanceado?")
    print("1) Sí")
    print("2) No")
    balanceado_input = int(input("> "))
    balanceado = True if balanceado_input == 1 else False

    # Formato de impedancias
    print("\nFormato de entrada de impedancias:")
    print("1) Rectangular (real, imag)")
    print("2) Polar (magnitud, ángulo en grados)")
    formato = int(input("> "))

    # Leer impedancias según tipo de carga y balanceo
    hilos = None
    if tipo_carga == "Y":
        print("\n¿El sistema es de 3 o 4 hilos?")
        print("1) 3 hilos (sin neutro)")
        print("2) 4 hilos (con neutro)")
        hilos_input = int(input("> "))
        hilos = 3 if hilos_input == 1 else 4

        if balanceado:
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
        # carga Δ
        if balanceado:
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
    resultado = calcular_tensiones_corrientes_potencias(
        Zs=Zs,
        V_linea_mag=Vlinea_mag,
        tipo_carga=tipo_carga,
        balanceado=balanceado,
        tipo_fuente=tipo_fuente,
        ang_v1_deg=ang_v1,
        hilos=hilos
    )

    imprimir_resultados_ordenados(resultado, tipo_carga, hilos)

    # Menú de graficado (opcional) - igual que antes
    while True:
        print("\n¿Desea graficar algún resultado?")
        print("1) Tensiones de fase y de línea")
        print("2) Corrientes de fase y de línea")
        print("3) Potencias por fase y total (instantánea)")
        print("4) Salir")
        opcion_graf = int(input("> "))
        if opcion_graf == 1:
            Vfasores_fuente = resultado.get("Vfase_fuente", [])
            Vlineas_fuente = resultado.get("Vlinea_fuente", [])
            if not Vfasores_fuente or not Vlineas_fuente:
                print("No hay tensiones disponibles para graficar.")
                continue
            from graficar import plot_fasores
            plot_fasores(
                Vfasores_fuente + Vlineas_fuente,
                nombres=[f"Vfase_{i+1}" for i in range(3)] + [f"Vlinea_{i+1}" for i in range(3)],
                titulo="Tensiones de Fase y Línea",
                xlabel="Voltios (Re)",
                ylabel="Voltios (Im)"
            )
        elif opcion_graf == 2:
            Ifases = resultado.get("Ifase") or resultado.get("Iramas_delta") or []
            Ilineas = resultado.get("Ilinea") or []
            if not Ifases or not Ilineas:
                print("No hay corrientes disponibles para graficar.")
                continue
            from graficar import plot_fasores
            plot_fasores(
                Ifases + Ilineas,
                nombres=[f"Ifase_{i+1}" for i in range(3)] + [f"Ilinea_{i+1}" for i in range(3)],
                titulo="Corrientes de Fase y Línea",
                xlabel="Amperios (Re)",
                ylabel="Amperios (Im)"
            )
        elif opcion_graf == 3:
            pot_fases = resultado.get("S_fase") or resultado.get("S_rama") or []
            if not pot_fases:
                print("No hay potencias por fase calculadas para graficar.")
                continue
            from graficar import plot_power_fases
            print("\n--- Gráfica de potencia instantánea por fase y total ---")
            freq = float(input("Frecuencia (Hz): "))
            V_complex_for_mag = resultado.get("Vfase_carga") or resultado.get("Vramas_delta") or resultado.get("Vfase_fuente") or resultado.get("Vlinea_fuente")
            I_complex_for_mag = resultado.get("Ifase") or resultado.get("Iramas_delta")
            Vms = [abs(v) for v in V_complex_for_mag]
            Ims = [abs(i) for i in I_complex_for_mag]
            phases_v = [math.degrees(cmath.phase(v)) for v in V_complex_for_mag]
            phases_i = [math.degrees(cmath.phase(i)) for i in I_complex_for_mag]
            plot_power_fases(Vms, Ims, phases_v, phases_i, freq)
        elif opcion_graf == 4:
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()