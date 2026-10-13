"""PMV / PPD / operative temperature (ISO 7730 / Fanger model) for Lab 2.

Run `python calculate_pmv_ppd.py` to print the lab's two tables.

Unit cheat-sheet used everywhere below
    temperatures : degC  (converted to K only inside the radiation term)
    pressures    : Pa
    heat fluxes  : W/m2 of body surface (DuBois area ~1.8 m2 for an adult)
    h_c          : W/(m2.K)      I_cl : m2.K/W      v : m/s
"""
import math

EPS = 0.0015  # convergence threshold on T_cl/100 [-] (= 0.15 K), value given in the lab sheet


def operative_temperature(t_a, t_mr, v):
    """Operative temperature t_o [degC]: the uniform-room temperature that would
    exchange the same dry heat with a person as the real room does.

    t_o = A*t_a + (1-A)*t_mr, where the weight A of the air temperature grows
    with air speed v [m/s] (more air movement -> convection dominates radiation).
    """
    if v < 0.2:
        a = 0.5
    elif v < 0.6:
        a = 0.6
    else:
        a = 0.7
    return a * t_a + (1 - a) * t_mr


def calculate_pmv_ppd(t_a, t_mr, v=0.15, rh=60, i_clo=0.5, m_met=1.2, details=False):
    """Return (pmv, ppd, t_o, n_iterations); with details=True also a dict of
    intermediate values (M, p_v, f_cl, h_c, t_cl, RL1..RL6, L, TS, t_cl history).

    t_a    air temperature [degC]
    t_mr   mean radiant temperature [degC] (average temperature of the room surfaces)
    v      relative air speed [m/s]
    rh     relative humidity [%]
    i_clo  clothing insulation [clo]   (1 clo = 0.155 m2.K/W)
    m_met  metabolic rate [met]        (1 met = 58.15 W/m2, a seated person at rest)

    PMV (Predicted Mean Vote, dimensionless) is the average vote on the 7-point
    scale -3 cold ... 0 neutral ... +3 hot. PPD [%] is the share of people who
    would be dissatisfied (voting beyond +-1) for that PMV.
    """
    # --- Step 2: unit conversions and preliminaries -------------------------
    m = m_met * 58.15                                  # metabolic heat production [W/m2]
    i_cl = 0.155 * i_clo                               # clothing insulation [m2.K/W]
    p_sat = math.exp(16.6536 - 4030.183 / (t_a + 235)) * 1000  # saturation pressure (Antoine) [Pa]
    p_v = rh / 100 * p_sat                             # partial water-vapour pressure [Pa]
    # f_cl: clothed surface / nude surface [-]; clothes enlarge the exchange area
    f_cl = 1 + 1.29 * i_cl if i_cl < 0.078 else 1.05 + 0.645 * i_cl

    # --- Step 3: iterate for the clothing surface temperature t_cl ----------
    # Energy balance of the clothing layer: heat through the clothes = heat lost outside,
    #   t_cl = 35.7 - 0.028*M - I_cl * (RL5 + RL6)       (35.7 degC ~ skin temperature)
    # RL5 and RL6 themselves depend on t_cl -> successive approximation (ISO 7730 scheme).
    # Temperatures are kept in K divided by 100 (xn, xf) so the T^4 term stays well scaled.
    t_a_k, t_mr_k = t_a + 273.15, t_mr + 273.15
    p1 = i_cl * f_cl
    p2 = p1 * 3.96                                    # radiation coefficient * insulation * area factor
    p3 = p1 * 100
    p4 = p1 * t_a_k
    p5 = 308.7 - 0.028 * m + p2 * (t_mr_k / 100) ** 4 # constant part of the balance (308.7 K = 35.7 degC + 273)
    t_cl0 = t_a_k + (35.5 - t_a) / (3.5 * (6.45 * i_cl + 0.1))  # first estimate [K]
    xn, xf = t_cl0 / 100, t_cl0 / 50                  # new / old value of T_cl/100
    h_c_forced = 12.1 * math.sqrt(v)                  # forced convection [W/m2.K]
    n_iter = 0
    history = [100 * xn - 273.15]                     # t_cl after each pass [degC], for plotting
    while abs(xn - xf) > EPS and n_iter < 150:
        n_iter += 1
        xf = (xf + xn) / 2                            # averaging damps the oscillation
        h_c_natural = 2.38 * abs(100 * xf - t_a_k) ** 0.25  # natural convection [W/m2.K]
        h_c = max(h_c_forced, h_c_natural)            # dominant mode wins
        xn = (p5 + p4 * h_c - p2 * xf**4) / (100 + p3 * h_c)  # solved balance for T_cl/100
        history.append(100 * xn - 273.15)
    t_cl = 100 * xn - 273.15                          # converged clothing temperature [degC]

    # --- Step 4: the six heat-loss paths [W/m2] -----------------------------
    rl5 = 3.96 * f_cl * (xn**4 - (t_mr_k / 100) ** 4)    # radiation clothes -> room surfaces
    rl6 = f_cl * h_c * (t_cl - t_a)                       # convection clothes -> room air
    rl1 = 3.05e-3 * (5733 - 6.99 * m - p_v)               # vapour diffusion through skin
    rl2 = 0.42 * (m - 58.15) if m > 58.15 else 0.0        # regulatory sweating (only above resting M)
    rl3 = 1.7e-5 * m * (5867 - p_v)                       # latent respiration
    rl4 = 0.0014 * m * (34 - t_a)                         # dry respiration

    # --- Step 5: thermal load -> PMV -> PPD ---------------------------------
    ts = 0.303 * math.exp(-0.036 * m) + 0.028             # sensation coefficient [m2/W]
    load = m - rl1 - rl2 - rl3 - rl4 - rl5 - rl6          # heat stored by the body [W/m2]; >0 -> feels warm
    pmv = ts * load
    ppd = 100 - 95 * math.exp(-0.03353 * pmv**4 - 0.2179 * pmv**2)

    out = (pmv, ppd, operative_temperature(t_a, t_mr, v), n_iter)
    if details:
        out += (dict(M=m, p_v=p_v, f_cl=f_cl, h_c=h_c, h_c_forced=h_c_forced, t_cl=t_cl, ts=ts, L=load,
                     RL1=rl1, RL2=rl2, RL3=rl3, RL4=rl4, RL5=rl5, RL6=rl6, history=history),)
    return out


def show(label, t_a, t_mr, **kw):
    """Print the results in the format required by the lab sheet."""
    pmv, ppd, t_o, n = calculate_pmv_ppd(t_a, t_mr, **kw)
    print(f"{label} (t_a={t_a} degC, t_mr={t_mr} degC)")
    print(f"PMV= {pmv:.3f}")
    print(f"PPD= {ppd:.1f} %")
    print(f"t_o= {t_o:.2f} degC")
    print(f"n iterations= {n}")
    print()


if __name__ == "__main__":
    show("Exterior (summer day)", 30, 30.5)
    # Interior: summer rule t_mr = t_a + 0.5; -0.5 < PMV < 0.5 for t_a ~ 23.25 .. 26 degC
    show("Interior (comfort)", 24.5, 25)
