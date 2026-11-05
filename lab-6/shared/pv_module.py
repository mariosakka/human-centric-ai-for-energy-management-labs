"""Reusable building blocks for Lab 6 (Kyocera KD230GX-LPB photovoltaic module, simplified NOCT model).
Every function only returns values: no printing, no plots. Temperatures in degrees C, irradiance G in W/m2.
G and tc may be numpy arrays."""
import math

# ---------------------------------------------------------------- data from the sheet
G_ST = 1000.0      # irradiance at standard test conditions (STC) [W/m2]
TC_ST = 25.0       # cell temperature at STC [C]: the reference of the coefficients, never 0 C
U0_ST = 36.9       # open-circuit voltage at STC [V]
ISC_ST = 8.36      # short-circuit current at STC [A]
PM_ST = 230.0      # rated power at STC [W]
NOCT = 45.0        # nominal operating cell temperature [C]
FF = 0.746         # fill factor, kept constant in the simplified model
MU_ISC = 0.0006 * ISC_ST     # temperature coefficient of Isc [A/K]  (+0.06 %/C)
MU_U0 = -0.0036 * U0_ST      # temperature coefficient of U0  [V/K]  (-0.36 %/C)

# hot-noon example quoted in the sheet
G_NOON, TA_NOON = 900.0, 30.0
# the spring morning of the exercise (wind speed w = 3 m/s is given but the NOCT model does not use it)
G_MORNING, TA_MORNING, W_MORNING = 500.0, 12.0, 3.0


def cell_temperature(g, ta, noct=NOCT):
    """NOCT model: tc = ta + (NOCT - 20) / 800 * G  [C]."""
    return ta + (noct - 20.0) / 800.0 * g


def photocurrent(g, tc):
    """I_L = (G / Gst) * [Isc_st + mu_Isc (tc - tc_st)]  [A]; equals the short-circuit current."""
    return g / G_ST * (ISC_ST + MU_ISC * (tc - TC_ST))


def open_circuit_voltage(tc):
    """U0 = U0_st + mu_U0 (tc - tc_st)  [V]; does not depend on G in the simplified model."""
    return U0_ST + MU_U0 * (tc - TC_ST)


def module_power(g, tc):
    """P_M = FF * U0 * Isc at irradiance g and a given cell temperature tc  [W]."""
    return FF * open_circuit_voltage(tc) * photocurrent(g, tc)


def operating_point(g, ta):
    """All quantities of one operating point as a dict: tc, i_l, u0, p_m, percent of rated power."""
    tc = cell_temperature(g, ta)
    i_l, u0 = photocurrent(g, tc), open_circuit_voltage(tc)
    p_m = FF * u0 * i_l
    return dict(g=g, ta=ta, tc=tc, i_l=i_l, u0=u0, p_m=p_m, percent_of_rated=100.0 * p_m / PM_ST)


def loss_split(g, ta):
    """Split the drop from the STC power into an irradiance part and a cell-temperature part.
    Two orders are possible and give slightly different shares:
      'irradiance_first': STC -> (g, 25 C) -> (g, tc);  'temperature_first': STC -> (1000, tc) -> (g, tc).
    Shares are in W; they add up to p_stc - p_m for each order. 'average' is the mean of both orders;
    'log' splits the drop in proportion to ln(factor), which does not depend on the order."""
    tc = cell_temperature(g, ta)
    p_stc, p_m = module_power(G_ST, TC_ST), module_power(g, tc)
    p_g_only, p_t_only = module_power(g, TC_ST), module_power(G_ST, tc)
    out = dict(tc=tc, p_stc=p_stc, p_m=p_m, drop=p_stc - p_m,
               irradiance_first=dict(irradiance=p_stc - p_g_only, temperature=p_g_only - p_m),
               temperature_first=dict(temperature=p_stc - p_t_only, irradiance=p_t_only - p_m))
    out["average"] = dict(
        irradiance=(out["irradiance_first"]["irradiance"] + out["temperature_first"]["irradiance"]) / 2,
        temperature=(out["irradiance_first"]["temperature"] + out["temperature_first"]["temperature"]) / 2)
    f_g, f_t = module_power(g, TC_ST) / p_stc, p_m / module_power(g, TC_ST)
    share_g = math.log(f_g) / math.log(f_g * f_t)
    out["log"] = dict(irradiance=share_g * out["drop"], temperature=(1 - share_g) * out["drop"])
    return out


def relative_efficiency(g, tc):
    """Output per unit of sunlight relative to STC: (P_M / G) / (P_M,st / G_st) from the model, in percent."""
    return 100.0 * (module_power(g, tc) / g) / (module_power(G_ST, TC_ST) / G_ST)
