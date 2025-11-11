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

def intensity_schedule(include_deload: bool = True):
    if include_deload:
        # como lo tenías
        return piecewise_constant([
            (0.0, 0.9),   # arranque
            (30.0, 1.2),  # hiper
            (60.0, 1.4),  # fuerza
            (90.0, 0.6),  # deload
            (110.0, 1.1),
            (140.0, 1.2)
        ])
    else:
        # igual que el caso "con deload" pero SIN bajón deload (mantenemos el bloque)
        return piecewise_constant([
            (0.0, 0.9),
            (30.0, 1.2),
            (60.0, 1.4),
            (90.0, 1.1),  # <- antes 0.6
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

def deload_effects(t0: float = 56.0, t1: float = 70.0, g_mult: float = 1.25, p_mult: float = 0.60):
    """Aumenta gamma y reduce phi en la ventana de deload."""
    def g_gamma(t: float) -> float:
        return g_mult if (t0 <= t <= t1) else 1.0
    def g_phi(t: float) -> float:
        return p_mult if (t0 <= t <= t1) else 1.0
    return g_gamma, g_phi


def microlesion_pulse(t0: float = 45.0, t1: float = 55.0, scale: float = 2.2):
    """Multiplica phi entre t0 y t1 (simula microlesión, bache notorio)."""
    def g(t: float) -> float:
        return scale if (t0 <= t <= t1) else 1.0
    return g


def beta_decay(t_half: float = 110.0, depth: float = 0.5, sharpness: float = 12.0):
    """
    Decaimiento suave de sensibilidad (0.5 = 50% del valor original hacia el final).
    Devuelve g(t) en [depth..1].
    """
    import math
    def g(t: float) -> float:
        # sigmoide suavizada; a la derecha de t_half cae hacia 'depth'
        return depth + (1.0 - depth) * (1.0 / (1.0 + math.exp((t - t_half)/sharpness)))
    return g
