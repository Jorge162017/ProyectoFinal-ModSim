# Default parameter sets for the SEIR-análogo de adaptación muscular
# Nota: Unidades en días y proporciones por día

from dataclasses import dataclass

@dataclass
class Params:
    # Población "susceptible" a mejorar (escala relativa, no demográfica)
    N: float = 1.0

    # Fuerza de estímulo (análoga a infección): beta * A(t)
    beta: float = 0.55          # sensibilidad al estímulo

    # Cadena de retraso E (k etapas, media 1/alpha)
    k: int = 5                  # orden de Erlang (>=1)
    alpha: float = 0.18         # velocidad por etapa (1/días)

    # Recuperación/adaptación desde I
    gamma: float = 0.30         # tasa de adaptación (1/días)

    # Recaída/retroceso desde I (fatiga/microlesión)
    phi: float = 0.10           # 0..1 proporción que regresa a S (riesgo neto)

    # Dinámica de rendimiento/masa (stocks agregados)
    # dM/dt = r_gain * R - r_loss * (M - M0)
    r_gain: float = 0.08
    r_loss: float = 0.02
    M0: float = 1.0             # baseline masa/índice (u.a.)

    # Adherencia base [0..1] (se modula por intervenciones/redes/ABM)
    adherence: float = 0.8

    # Intensidad/volumen relativo del bloque de entrenamiento [0..2]
    block_intensity: float = 1.0

    # Duración de simulación
    t_max: float = 180.0
    dt: float = 0.25            # paso (días)
