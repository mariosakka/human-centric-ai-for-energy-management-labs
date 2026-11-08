"""Reusable building blocks for Lab 2 (psychrometrics of the sheet's two outdoor days, and PMV-based comfort ranges).
Every function only returns values: no printing, no plots."""
import numpy as np
import pandas as pd
from scipy.optimize import brentq

from calculate_pmv_ppd import calculate_pmv_ppd

# ---------------------------------------------------------------- data from the sheet
T_TAB = np.arange(-6, 41, 2)           # table of saturation pressure: temperature [C]
P_TAB = np.array([390.9, 454.9, 527.9, 611.2, 706, 813.5, 935.3, 1073, 1228, 1403, 1599, 1819,
                  2065, 2339, 2645, 2986, 3364, 3783, 4247, 4760, 5325, 5948, 6633, 7385])   # [Pa]
P_ATM = 1e5                            # 1 bar [Pa]

HOURS = np.arange(1, 25)               # hour of the day (UTC)
T_SUMMER = np.array([22.5, 21.8, 21, 21, 20.7, 20.9, 22, 23.3, 24.4, 25.6, 26.3, 26.9, 27.3, 27.7, 27.9, 27.9, 27.3, 26.7, 25.9, 24.6, 23.3, 22, 20.6, 19.3])
RH_SUMMER = np.array([83, 89, 90, 91, 89, 86, 80, 80, 62, 55, 54, 53, 48, 47, 46, 44, 56, 46, 49, 53, 53, 55, 59, 60])
T_WINTER = np.array([3.5, 2.9, 2.2, 1.9, 1.6, 1.3, 1.1, 1.4, 3.3, 5.3, 6.7, 7.4, 7.9, 7.9, 7.7, 7, 5.8, 5.3, 4.8, 4.3, 3.8, 3.3, 2.8, 2.3])
RH_WINTER = np.array([79, 81, 84, 81, 83, 83, 85, 84, 77, 72, 73, 74, 69, 66, 67, 74, 78, 77, 77, 81, 82, 87, 86, 85])

ROOM_AIR_KG = 84.14                    # air mass of the 6 x 4 x 3 m room (A1) [kg]
LATENT_HEAT = 2500                     # heat released by 1 kg of condensing vapour [kJ/kg]
RL_KEYS = ["RL1", "RL2", "RL3", "RL4", "RL5", "RL6"]


# ---------------------------------------------------------------- moist air
def p_sat(t):
    """Saturation pressure [Pa] at temperature t [C], interpolated in the sheet's table."""
    return np.interp(t, T_TAB, P_TAB)


def t_sat(pv):
    """Inverse of p_sat: temperature [C] at which the vapour pressure pv [Pa] saturates the air (the dew point)."""
    return np.interp(pv, P_TAB, T_TAB)


def humidity_ratio(pv, p=P_ATM):
    """Humidity ratio [kg water / kg dry air] for vapour pressure pv [Pa]."""
    return 0.622 * pv / (p - pv)


def enthalpy(t, x):
    """Enthalpy [kJ/kg dry air] of air at t [C] with humidity ratio x [kg/kg]."""
    return t + x * (2500 + 1.84 * t)


def day_x_h(t, phi):
    """Hourly humidity ratio [g/kg] and enthalpy [kJ/kg] from temperature t [C] and relative humidity phi [%]."""
    x = humidity_ratio(phi / 100 * p_sat(t))
    return 1000 * x, enthalpy(t, x)


def daily(t, phi):
    """Hourly curves of one day as a dict: t, RH, x [g/kg], dew point tdp, gap = t - tdp, enthalpy h."""
    pv = phi / 100 * p_sat(t)
    x = 1000 * humidity_ratio(pv)
    tdp = t_sat(pv)
    return dict(t=t, RH=phi, x=x, tdp=tdp, gap=t - tdp, h=enthalpy(t, x / 1000))


def day_table(t, phi):
    """Hourly table of one day (DataFrame): t, phi, p_v, x, dew point, enthalpy."""
    pv = phi / 100 * p_sat(t)
    x = humidity_ratio(pv)
    return pd.DataFrame({"hour (UTC)": HOURS, "t": t, "phi": phi, "p_v [Pa]": pv.round(0), "x [g/kg]": (1000 * x).round(2),
                         "t_dp": t_sat(pv).round(1), "h [kJ/kg]": enthalpy(t, x).round(1)})


def correlation(d, a, b):
    """Correlation coefficient between the daily curves d[a] and d[b]."""
    return np.corrcoef(d[a], d[b])[0, 1]


def condensation(t0, phi0, t_end):
    """Air at t0 [C] and phi0 (0..1) cooled to t_end [C]: (x_now, x_end, drop) in g/kg dry air.
    x_now is what the air carries, x_end the most it can carry at t_end, drop the part that turns to liquid."""
    x_now = 1000 * humidity_ratio(phi0 * p_sat(t0))
    x_end = 1000 * humidity_ratio(p_sat(t_end))
    return x_now, x_end, x_now - x_end


# ---------------------------------------------------------------- comfort
def comfort_range(bracket=(15, 30), **kw):
    """Air temperatures (t_lo, t_hi) [C] where -0.5 < PMV < 0.5, with t_mr = t_a + 0.5.
    kw are passed to calculate_pmv_ppd (i_clo, m_met, ...); bracket is the search interval for the root."""
    f = lambda ta: calculate_pmv_ppd(ta, ta + 0.5, **kw)[0]
    return brentq(lambda t: f(t) + 0.5, *bracket), brentq(lambda t: f(t) - 0.5, *bracket)


def factor_sensitivity(base, step):
    """Change of each heat loss RL1..RL6 [W/m2] when one factor of `base` (dict of calculate_pmv_ppd arguments)
    is changed by its step ({label: (argument, step)}): array of shape (6, number of factors)."""
    *_, d0 = calculate_pmv_ppd(**base, details=True)
    return np.array([[calculate_pmv_ppd(**{**base, p: base[p] + s}, details=True)[-1][k] - d0[k] for p, s in step.values()]
                     for k in RL_KEYS])
