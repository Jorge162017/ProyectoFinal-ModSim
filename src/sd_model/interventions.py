# Schedules y funciones que modulan A(t), gamma(t), phi(t) en el tiempo.

from typing import Callable, List, Tuple

def piecewise_constant(schedule: List[Tuple[float, float]]) -> Callable[[float], float]:
    """
    Crea una función f(t) por tramos.
    schedule: lista de (t_inicio, valor). Asume orden ascendente.
    """
    def f(t: float) -> float:
        val = schedule[0][1]
        for t0, v in schedule:
            if t >= t0:
                val = v
            else:
                break
        return val
    return f

def adherence_schedule():
    """Bloques hiper -> fuerza -> deload (adherencia/intensidad)"""
    # t en días
    return piecewise_constant([
        (0.0, 0.85),     # Arranque
        (30.0, 0.90),    # Hiper
        (60.0, 0.80),    # Fuerza (peor adherencia pero más intensidad)
        (90.0, 0.95),    # Deload: alta adherencia
        (110.0, 0.88),
        (140.0, 0.90)
    ])

def intensity_schedule():
    return piecewise_constant([
        (0.0, 0.9),    # arranque
        (30.0, 1.2),   # hiper
        (60.0, 1.4),   # fuerza
        (90.0, 0.6),   # deload
        (110.0, 1.1),
        (140.0, 1.2)
    ])

def protein_schedule():
    # 1.0 = suficiente; <1 deficiencia leve reduce respuesta
    return piecewise_constant([
        (0.0, 0.9),
        (45.0, 1.0),
        (120.0, 0.95),
    ])

def deload_effects():
    """
    Devuelve funciones multiplicativas para gamma y phi.
    Durante deload (t∈[90,100]) aumenta gamma y reduce phi.
    """
    def g_gamma(t: float) -> float:
        return 1.3 if 90.0 <= t <= 100.0 else 1.0
    def g_phi(t: float) -> float:
        return 0.6 if 90.0 <= t <= 100.0 else 1.0
    return g_gamma, g_phi

def microlesion_pulse(t0=50.0, t1=65.0, scale=1.8):
    """Multiplica phi entre t0 y t1 (simula microlesión)."""
    def g(t: float) -> float:
        return scale if (t0 <= t <= t1) else 1.0
    return g

def beta_decay(t_half=90.0):
    """Decaimiento suave de sensibilidad (estancamiento)."""
    import math
    def g(t: float) -> float:
        return 1.0 / (1.0 + math.exp((t - t_half)/10.0))
    return g
