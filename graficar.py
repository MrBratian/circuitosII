import numpy as np
import matplotlib.pyplot as plt

def instantaneous_power(Vm, Im, freq, phase_v=0, phase_i=0, duration=0.05, samples=1000):
    t = np.linspace(0, duration, samples)
    omega = 2 * np.pi * freq
    v = Vm * np.sin(omega * t + np.deg2rad(phase_v))
    i = Im * np.sin(omega * t + np.deg2rad(phase_i))
    p = v * i
    return t, v, i, p

def plot_power(Vm, Im, freq, phase_v=0, phase_i=0, duration=0.05, samples=1000):
    t, v, i, p = instantaneous_power(Vm, Im, freq, phase_v, phase_i, duration, samples)
    plt.figure(figsize=(10,6))
    plt.plot(t, v, label='Voltaje Instantáneo (V)')
    plt.plot(t, i, label='Corriente Instantánea (A)')
    plt.plot(t, p, label='Potencia Instantánea (W)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Valor')
    plt.title('Gráfica de Potencia Instantánea, Voltaje y Corriente')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_fasores(fasores, nombres=None, titulo="Diagrama Fasorial", xlabel="Parte Real", ylabel="Parte Imaginaria"):
    plt.figure(figsize=(8,8))
    ax = plt.gca()
    ax.set_aspect('equal')
    max_val = max([abs(f) for f in fasores]) * 1.2
    plt.xlim(-max_val, max_val)
    plt.ylim(-max_val, max_val)
    plt.axhline(0, color='gray', lw=0.5)
    plt.axvline(0, color='gray', lw=0.5)
    colores = ['b', 'g', 'r', 'm', 'c', 'y', 'k']
    for idx, f in enumerate(fasores):
        color = colores[idx % len(colores)]
        plt.arrow(0, 0, f.real, f.imag, head_width=max_val*0.05, head_length=max_val*0.08, fc=color, ec=color)
        if nombres:
            plt.text(f.real*1.05, f.imag*1.05, nombres[idx], fontsize=12, color=color)
        else:
            plt.text(f.real*1.05, f.imag*1.05, f"F{idx+1}", fontsize=12, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.grid(True)
    plt.show()

def plot_power_vectors(potencias, nombres=None):
    """
    potencias: lista de números complejos (S = P + jQ)
    nombres: lista de nombres para cada vector
    """
    plt.figure(figsize=(8,8))
    ax = plt.gca()
    ax.set_aspect('equal')
    max_val = max([abs(S) for S in potencias]) * 1.2 if potencias else 1
    plt.xlim(-max_val, max_val)
    plt.ylim(-max_val, max_val)
    plt.axhline(0, color='gray', lw=0.5)
    plt.axvline(0, color='gray', lw=0.5)
    for idx, S in enumerate(potencias):
        plt.arrow(0, 0, S.real, S.imag, head_width=max_val*0.05, head_length=max_val*0.08, fc='b', ec='b')
        if nombres:
            plt.text(S.real*1.05, S.imag*1.05, nombres[idx], fontsize=12)
        else:
            plt.text(S.real*1.05, S.imag*1.05, f"S{idx+1}", fontsize=12)
    plt.xlabel('Potencia Activa (P) [W]')
    plt.ylabel('Potencia Reactiva (Q) [var]')
    plt.title('Diagrama Fasorial de Potencias')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Ejemplo: Vm=311V, Im=10A, freq=50Hz, desfase=30°
    plot_power(Vm=311, Im=10, freq=50, phase_v=0, phase_i=30)

    # Ejemplo de uso para plot_power_vectors
    S1 = 1000 + 500j
    S2 = 800 + 200j
    S3 = 1200 + 700j
    plot_fasores([S1, S2, S3], nombres=["Fase A", "Fase B", "Fase C"], titulo="Diagrama Fasorial de Potencias", xlabel="Potencia Activa (P) [W]", ylabel="Potencia Reactiva (Q) [var]")