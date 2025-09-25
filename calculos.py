import cmath
import math
from typing import List, Tuple, Dict

def phasor(magnitude: float, angle_deg: float) -> complex:
    return cmath.rect(magnitude, math.radians(angle_deg))

def generar_fuentes(V_linea_mag: float, tipo_fuente: str = "Y", ang_v1_deg: float = 0.0
                  ) -> Tuple[List[complex], List[complex]]:
    """
    Retorna (Vfase_fuente_list, Vlinea_fuente_list).

    - tipo_fuente == 'Y': V_linea_mag es V_LL; se calcula Vfase = V_LL/√3 y Vlinea = Vab,Vbc,Vca con los ángulos adecuados.
    - tipo_fuente == 'D': V_linea_mag se interpreta como V_LL; Vlinea se devuelve tal cual y además se
      calcula Vfase_equivalente = V_LL/√3 ∠(θ_LL - 30°) para modelar la delta vista por una carga Y.
    """
    angulos_linea = [ang_v1_deg, ang_v1_deg - 120.0, ang_v1_deg + 120.0]

    if tipo_fuente.upper() == "Y":
        # Vfase (fase a neutro) = V_LL / sqrt(3)
        Vfase_mag = V_linea_mag / math.sqrt(3)
        Vfase = [phasor(Vfase_mag, a) for a in [ang_v1_deg, ang_v1_deg - 120.0, ang_v1_deg + 120.0]]
        # Vlinea (Vab, Vbc, Vca) con ángulo fase+30°
        Vlinea_angles = [ang_v1_deg + 30.0, ang_v1_deg - 90.0, ang_v1_deg + 150.0]
        Vlinea = [phasor(V_linea_mag, a) for a in Vlinea_angles]
        return Vfase, Vlinea

    # Delta: Vlinea tal cual (Vab, Vbc, Vca)
    Vlinea = [phasor(V_linea_mag, a) for a in angulos_linea]
    # Vfase equivalente (para usar con cargas Y conectadas a esta fuente Δ)
    theta_a = ang_v1_deg - 30.0
    Vfase_mag_eq = V_linea_mag / math.sqrt(3)
    Vfase = [
        phasor(Vfase_mag_eq, theta_a),
        phasor(Vfase_mag_eq, theta_a - 120.0),
        phasor(Vfase_mag_eq, theta_a + 120.0)
    ]
    return Vfase, Vlinea

def ensure_three(zs: List[complex]) -> List[complex]:
    if len(zs) == 1:
        return [zs[0], zs[0], zs[0]]
    if len(zs) != 3:
        raise ValueError("Se esperan 1 o 3 impedancias para la carga.")
    return zs

def potencia_por_fase(Vfase_list: List[complex], Ifase_list: List[complex]) -> Tuple[List[complex], complex]:
    potencias = []
    Stot = 0+0j
    for V, I in zip(Vfase_list, Ifase_list):
        S = V * I.conjugate()
        potencias.append(S)
        Stot += S
    return potencias, Stot

# ------------------ CARGA Y ------------------
def calcular_y(
    Zs: List[complex],
    Vfase_fuente: List[complex],
    hilos: int = 4,
    balanceado: bool = True
) -> Tuple[List[complex], List[complex], List[complex], complex, complex]:
    """
    Retorna: (Vcarga_por_fase, Ifase_list, Ilinea_list, VnN, In)
    - VnN: corrimiento de neutro (tensión del neutro de carga respecto al neutro de fuente)
    - In: corriente de neutro (o la que circularía si existiera)
    """
    Zs = ensure_three(Zs)

    # 4 hilos (con neutro)
    if hilos == 4:
        Vc = Vfase_fuente
        If = [Vc[i] / Zs[i] for i in range(3)]
        Iline = If.copy()
        VnN = 0+0j
        In = -sum(If)
        return Vc, If, Iline, VnN, In

    # 3 hilos (sin neutro)
    if balanceado:
        Vc = Vfase_fuente
        VnN = 0+0j
    else:
        Ya, Yb, Yc = 1/Zs[0], 1/Zs[1], 1/Zs[2]
        Ytot = Ya + Yb + Yc
        # VnN = (Van/Za + Vbn/Zb + Vcn/Zc) / (1/Za + 1/Zb + 1/Zc)
        VnN = (Vfase_fuente[0]*Ya + Vfase_fuente[1]*Yb + Vfase_fuente[2]*Yc) / Ytot
        Vc = [Vfase_fuente[i] - VnN for i in range(3)]

    If = [Vc[i] / Zs[i] for i in range(3)]
    # Para carga Y, las corrientes de línea coinciden con corrientes de fase (cada conductor alimenta su fase)
    Iline = If.copy()
    In = -sum(If)  # corriente de neutro "conceptual" (la que circularía si existiera conductor neutro)
    return Vc, If, Iline, VnN, In

# ------------------ CARGA Δ ------------------
def calcular_delta(
    Zs: List[complex],
    Vlinea_fuente: List[complex],
    balanceado: bool = True
) -> Tuple[List[complex], List[complex], List[complex]]:
    Zs = ensure_three(Zs)

    # Tensiones en ramas del delta = tensiones línea-a-línea
    Vramas = Vlinea_fuente.copy()
    Ifases_rama = [Vramas[i] / Zs[i] for i in range(3)]
    Iline = [Ifases_rama[0] - Ifases_rama[2],
             Ifases_rama[1] - Ifases_rama[0],
             Ifases_rama[2] - Ifases_rama[1]]
    return Vramas, Ifases_rama, Iline

# ------------------ FUNCION PRINCIPAL ------------------
def calcular_tensiones_corrientes_potencias(
    Zs: List[complex],
    V_linea_mag: float,
    tipo_carga: str = "Y",
    balanceado: bool = True,
    tipo_fuente: str = "Y",
    ang_v1_deg: float = 0.0,
    hilos: int = 4,
    usar_aron: bool = False
) -> Dict[str, object]:
    """
    Devuelve un dict con claves (dependiendo del caso):
    - Vfase_fuente, Vlinea_fuente
    - Si carga Y: Vfase_carga, Ifase, Ilinea, S_fase, S_total, VnN, VNn, In
    - Si carga Δ: Vramas_delta, Iramas_delta, Ilinea, S_rama, S_total
    """
    tipo_carga = tipo_carga.upper()
    tipo_fuente = tipo_fuente.upper()

    Vfase_fuente, Vlinea_fuente = generar_fuentes(V_linea_mag, tipo_fuente, ang_v1_deg)
    resultado: Dict[str, object] = {
        "Vfase_fuente": Vfase_fuente,
        "Vlinea_fuente": Vlinea_fuente
    }

    if tipo_carga == "Y":
        Vcarga, Ifase, Ilinea, VnN, In = calcular_y(Zs, Vfase_fuente, hilos=hilos, balanceado=balanceado)
        S_fase, S_total = potencia_por_fase(Vcarga, Ifase)
        resultado.update({
            "Vfase_carga": Vcarga,
            "Ifase": Ifase,
            "Ilinea": Ilinea,
            "S_fase": S_fase,
            "S_total": S_total,
            "VnN": VnN,
            "VNn": -VnN,
            "In": In
        })
        return resultado

    # Delta load
    Vramas, Iramas, Ilinea = calcular_delta(Zs, Vlinea_fuente, balanceado=balanceado)
    S_rama, S_total = potencia_por_fase(Vramas, Iramas)
    resultado.update({
        "Vramas_delta": Vramas,
        "Iramas_delta": Iramas,
        "Ilinea": Ilinea,
        "S_rama": S_rama,
        "S_total": S_total
    })
    return resultado
