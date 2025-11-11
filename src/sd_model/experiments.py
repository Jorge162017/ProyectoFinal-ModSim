import numpy as np
from .params import Params
from .seir_muscle import MuscleSEIRModel
from .interventions import adherence_schedule, intensity_schedule, protein_schedule, deload_effects, piecewise_constant

def build_A():
    adh = adherence_schedule()
    inten = intensity_schedule()
    prot = protein_schedule()
    def A(t: float) -> float:
        return np.clip(adh(t) * inten(t) * prot(t), 0.0, 2.0)
    return A

def base_run(params: Params = None):
    if params is None:
        params = Params()
    A = build_A()
    g_gamma, g_phi = deload_effects()
    model = MuscleSEIRModel(params, A, g_gamma, g_phi)
    return model.simulate()

def no_delay_run(params: Params = None):
    if params is None:
        params = Params()
    # k=1 y alpha grande ~ sin retraso
    params2 = Params(**{**params.__dict__})
    params2.k = 1
    params2.alpha = 5.0
    A = build_A()
    g_gamma, g_phi = deload_effects()
    model = MuscleSEIRModel(params2, A, g_gamma, g_phi)
    return model.simulate()

def deload_toggle_run(use_deload: bool, params: Params = None):
    if params is None:
        params = Params()
    A = build_A()
    if use_deload:
        g_gamma, g_phi = deload_effects()
    else:
        g_gamma = lambda t: 1.0
        g_phi = lambda t: 1.0
    model = MuscleSEIRModel(params, A, g_gamma, g_phi)
    return model.simulate()

def constant_A_run(adh=0.8, inten=1.0, prot=1.0, params: Params = None):
    if params is None:
        params = Params()
    const = np.clip(adh*inten*prot, 0.0, 2.0)
    A = piecewise_constant([(0.0, const)])
    g_gamma, g_phi = deload_effects()
    model = MuscleSEIRModel(params, A, g_gamma, g_phi)
    return model.simulate()

# ---------------- Metrics -----------------
def time_to_peak(x_t, t):
    idx = int(np.argmax(x_t))
    return float(t[idx]), float(x_t[idx])

def auc(y, t):
    return float(np.trapz(y, t))

def metrics(out, M0=1.0):
    t = out["t"]
    R = out["R"]
    I = out["I"]
    M = out["M"]
    t_peak_R, peak_R = time_to_peak(R, t)
    t_peak_M, peak_M = time_to_peak(M, t)
    deltaM = float(M[-1] - M0)
    auc_I = auc(I, t)
    return {
        "t_peak_R": t_peak_R,
        "peak_R": peak_R,
        "t_peak_M": t_peak_M,
        "peak_M": peak_M,
        "deltaM_final": deltaM,
        "AUC_I": auc_I
    }

# ---------------- Sensitivity -----------------
def sweep_beta_phi(beta_vals, phi_vals, params: Params = None):
    if params is None:
        params = Params()
    res = np.zeros((len(beta_vals), len(phi_vals)))
    for i, b in enumerate(beta_vals):
        for j, f in enumerate(phi_vals):
            p2 = Params(**{**params.__dict__})
            p2.beta = float(b)
            p2.phi = float(f)
            out = base_run(p2)
            res[i, j] = out["M"][-1]  # masa final
    return res

from .interventions import microlesion_pulse, beta_decay

def scenario_microlesion(params: Params=None):
    if params is None:
        params = Params()
    A = build_A()
    g_gamma, g_phi = deload_effects()
    # Combinar pulso de microlesión sobre phi
    pulse = microlesion_pulse()
    phi_mod = lambda t: g_phi(t) * pulse(t)
    model = MuscleSEIRModel(params, A, g_gamma, phi_mod)
    return model.simulate()

def scenario_stagnation(params: Params=None):
    if params is None:
        params = Params()
    # Reduce beta efectivamente multiplicándose por una sigmoide en el tiempo
    p2 = Params(**{**params.__dict__})
    A = build_A()
    g_gamma, g_phi = deload_effects()
    # Emular decaimiento en beta con A(t)
    dec = beta_decay()
    def A_mod(t: float):
        return A(t) * dec(t)
    model = MuscleSEIRModel(p2, A_mod, g_gamma, g_phi)
    return model.simulate()
