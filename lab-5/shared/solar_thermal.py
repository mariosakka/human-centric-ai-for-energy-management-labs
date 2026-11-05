"""Reusable building blocks for Lab 5 (flat-plate solar thermal collector, characteristic curve).
Every function only returns values: no printing, no plots."""

# ---------------------------------------------------------------- data from the sheet
DOUBLE = dict(name="double-glazed, selective coating", f_r_tau_alpha=0.70, f_r_u_l=3.5)
SINGLE = dict(name="single-glazed", f_r_tau_alpha=0.75, f_r_u_l=6.0)

# operating points [G_T in W/m2, T_i and T_a in degC]
WINTER = dict(g_t=600.0, t_i=50.0, t_a=5.0)               # (a) to (c), and (e), (f) for both collectors
SINGLE_OWN = dict(g_t=750.0, t_i=45.0, t_a=20.0, q_u=412.0)   # (d): the single-glazed collector's own day


# ---------------------------------------------------------------- characteristic curve
def reduced_temperature(t_i, t_a, g_t):
    """x = (T_i - T_a) / G_T [K m2/W]. A difference in degC equals the same difference in K."""
    return (t_i - t_a) / g_t


def efficiency(collector, x):
    """eta = F_R(tau alpha) - F_R U_L x (dimensionless; works on a number or a numpy array)."""
    return collector["f_r_tau_alpha"] - collector["f_r_u_l"] * x


def useful_power(collector, g_t, t_i, t_a):
    """q_u = eta G_T [W per m2 of collector]."""
    return efficiency(collector, reduced_temperature(t_i, t_a, g_t)) * g_t


def crossing(a, b):
    """x where the efficiency lines of collectors a and b are equal; None if the lines are parallel."""
    d_slope = a["f_r_u_l"] - b["f_r_u_l"]
    if d_slope == 0:
        return None
    return (a["f_r_tau_alpha"] - b["f_r_tau_alpha"]) / d_slope


def stagnation_x(collector):
    """x where eta reaches 0: the collector delivers nothing (its losses eat all the absorbed sun)."""
    return collector["f_r_tau_alpha"] / collector["f_r_u_l"]


def better_collector(a, b, x):
    """The collector with the higher efficiency at reduced temperature x."""
    return a if efficiency(a, x) >= efficiency(b, x) else b


def efficiency_from_power(q_u, g_t):
    """eta = q_u / G_T, used to check the sheet's q_u = 412 W/m2 of the single-glazed collector."""
    return q_u / g_t
