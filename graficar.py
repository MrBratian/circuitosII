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

if __name__ == "__main__":
    # Ejemplo: Vm=311V, Im=10A, freq=50Hz, desfase=30°
    plot_power(Vm=311, Im=10, freq=50, phase_v=0, phase_i=30)