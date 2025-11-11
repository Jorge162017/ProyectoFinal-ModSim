import numpy as np
from dataclasses import dataclass
from typing import Dict, Callable, Tuple
from .params import Params

@dataclass
class State:
    S: float
    E: np.ndarray  # vector de tamaño k
    I: float
    R: float
    M: float       # masa/rendimiento proxy

def rk4_step(f, t, y, dt):
    k1 = f(t, y)
    k2 = f(t + dt/2, y + dt * k1 / 2)
    k3 = f(t + dt/2, y + dt * k2 / 2)
    k4 = f(t + dt,   y + dt * k3)
    return y + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

class MuscleSEIRModel:
    def __init__(self, params: Params,
                 A_func: Callable[[float], float],
                 gamma_mod: Callable[[float], float] = lambda t: 1.0,
                 phi_mod: Callable[[float], float] = lambda t: 1.0):
        self.p = params
        self.A = A_func
        self.gm = gamma_mod
        self.pm = phi_mod

    def _derivatives(self, t: float, y: np.ndarray) -> np.ndarray:
        p = self.p
        k = p.k
        # y = [S, E1..Ek, I, R, M]
        S = y[0]
        E = y[1:1+k]
        I = y[1+k]
        R = y[2+k]
        M = y[3+k]

        A_t = self.A(t)  # adherencia*intensidad*proteína etc.
        lam = p.beta * A_t

        alpha = p.alpha
        gamma = p.gamma * self.gm(t)
        phi = p.phi * self.pm(t)

        dS = -lam * S + phi * I
        dE = np.zeros_like(E)
        # Cadena Erlang
        dE[0] = lam * S - alpha * E[0]
        for i in range(1, k):
            dE[i] = alpha * E[i-1] - alpha * E[i]
        dI = alpha * E[-1] - gamma * (1.0 - phi) * I - phi * I
        dR = gamma * (1.0 - phi) * I

        # Masa / rendimiento
        dM = p.r_gain * dR - p.r_loss * (M - p.M0)

        dydt = np.concatenate(([dS], dE, [dI, dR, dM]))
        return dydt

    def simulate(self, S0=0.99, I0=0.01, R0=0.0, M0=None):
        p = self.p
        if M0 is None:
            M0 = p.M0
        E0 = np.zeros(p.k)
        y0 = np.concatenate(([S0], E0, [I0, R0, M0]))

        steps = int(p.t_max / p.dt) + 1
        t = np.linspace(0, p.t_max, steps)
        y_hist = np.zeros((steps, 3 + p.k + 1))
        y = y0.copy()
        for i in range(steps):
            y_hist[i] = y
            y = rk4_step(self._derivatives, t[i], y, p.dt)

        # Retorna dict con series
        out = {
            "t": t,
            "S": y_hist[:, 0],
            "E": y_hist[:, 1:1+p.k],
            "I": y_hist[:, 1+p.k],
            "R": y_hist[:, 2+p.k],
            "M": y_hist[:, 3+p.k],
        }
        return out
