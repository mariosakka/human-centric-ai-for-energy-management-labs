"""Reusable building blocks for Lab 4 (steady-state heat loss of a house + human-centred setpoint).
Every function only returns values: no printing, no plots."""
import pandas as pd
from scipy.optimize import brentq

from calculate_pmv_ppd import calculate_pmv_ppd

# ---------------------------------------------------------------- data from the sheet
T_E = 5.0          # exterior air [C]
T_I = 24.0         # indoor air [C]
T_SOIL = 11.0      # soil temperature under the house [C] (10 to 12 in the sheet)
ALPHA_E = 24.0     # exterior convection [W/m2K]
ALPHA_I_WALL = 8.0
ALPHA_I_FLOOR = 6.0

A_WALL_GROSS = 4 * (3 * 6)     # four walls 3 m x 6 m [m2]
A_WIN_EAST = 1.0 * 2.0
A_WIN_SOUTH = 1.0 * 2.0
A_FLOOR = 6.0 * 6.0

# (name, thickness [m], conductivity [W/mK]), from outside to inside
WALL = [("decorative plaster", 0.005, 0.024), ("polystyrene EPS", 0.100, 0.040), ("mortar exterior", 0.003, 0.870),
        ("AAC masonry", 0.250, 0.150), ("mortar interior", 0.002, 0.870)]
FLOOR = [("hardwood", 0.02, 0.23), ("cement screed", 0.05, 0.93), ("polystyrene XPS", 0.10, 0.025),
         ("reinforced concrete", 0.20, 2.03), ("gravel", 0.20, 0.70), ("soil 0 to -3 m", 2.43, 2.0), ("soil -3 to -7 m", 4.0, 4.0)]
CEILING = [("mortar interior", 0.002, 0.87), ("reinforced concrete", 0.20, 2.03), ("cement screed", 0.05, 0.93), ("hardwood", 0.02, 0.23)]

C1, C2, C3 = 0.9, 0.6, 0.6      # double glazing, light blinds, metallic frame
K_WIN = 2.56                    # window U-value [W/m2K]
WINDOWS = {"east": dict(area=A_WIN_EAST, m=0.3, i_t=55.0), "south": dict(area=A_WIN_SOUTH, m=0.7, i_t=380.0)}

MATERIALS = {   # conductivity [W/mK], from the sheet
    "cement plaster": 0.80, "reinforced concrete": 2.03, "solid brick": 0.70, "hollow brick": 0.35,
    "AAC": 0.15, "mineral wool": 0.036, "polystyrene EPS": 0.04, "polystyrene XPS": 0.025}


# ---------------------------------------------------------------- layers and U-value
def layer_table(layers):
    """Layer list -> DataFrame with R = thickness / conductivity [m2K/W]."""
    df = pd.DataFrame(layers, columns=["layer", "delta_m", "lambda_W_mK"])
    df["R_m2K_W"] = df.delta_m / df.lambda_W_mK
    return df


def total_resistance(layers, alpha_i, alpha_e=None):
    """Surface-to-surface plus film resistances: 1/alpha_i + sum(delta/lambda) (+ 1/alpha_e if given)."""
    r = 1 / alpha_i + layer_table(layers).R_m2K_W.sum()
    return r + (1 / alpha_e if alpha_e else 0.0)


def k_value(layers, alpha_i, alpha_e=None):
    """Overall heat transfer coefficient k [W/m2K]."""
    return 1 / total_resistance(layers, alpha_i, alpha_e)


def temperature_profile(layers, alpha_i, alpha_e, t_in, t_out):
    """Temperature at each interface, from inside to outside: returns DataFrame (position, label, temp)."""
    q = (t_in - t_out) * k_value(layers, alpha_i, alpha_e)       # W/m2
    inside = list(reversed(layers))
    pts = [("indoor air", t_in), ("inner surface", t_in - q / alpha_i)]
    t = pts[-1][1]
    for name, d, lam in inside:
        t -= q * d / lam
        pts.append((f"after {name}", t))
    pts.append(("outdoor air", t_out))
    return pd.DataFrame(pts, columns=["point", "temp"])


def with_insulation(layers, name, thickness):
    """Copy of a layer list with the layer called `name` set to a new thickness (0 removes its effect)."""
    return [(n, thickness if n == name else d, lam) for n, d, lam in layers]


def without_layer(layers, name):
    return [row for row in layers if row[0] != name]


# ---------------------------------------------------------------- loads (positive = heat lost)
def wall_flux(t_i=T_I, t_e=T_E, layers=WALL):
    """Q1: heat flux through the opaque wall [W/m2]."""
    return k_value(layers, ALPHA_I_WALL, ALPHA_E) * (t_i - t_e)


def wall_load(t_i=T_I, t_e=T_E, layers=WALL):
    """Opaque wall: net area x flux [W]."""
    a_net = A_WALL_GROSS - A_WIN_EAST - A_WIN_SOUTH
    return wall_flux(t_i, t_e, layers) * a_net


def window_load(side, t_i=T_I, t_e=T_E):
    """One window [W]: -c1 c2 c3 m A I_T + k A (t_i - t_e). Negative = net gain."""
    w = WINDOWS[side]
    return -C1 * C2 * C3 * w["m"] * w["area"] * w["i_t"] + K_WIN * w["area"] * (t_i - t_e)


def floor_load(t_i=T_I, t_soil=T_SOIL, layers=FLOOR):
    """Heated floor to the soil [W]."""
    return k_value(layers, ALPHA_I_FLOOR) * A_FLOOR * (t_i - t_soil)


def ceiling_load(t_i=T_I, t_above=T_I, layers=CEILING):
    """Ceiling towards the heated upper floor [W]: zero when both floors have the same temperature."""
    return k_value(layers, ALPHA_I_FLOOR) * A_FLOOR * (t_i - t_above)


def total_load(t_i=T_I, t_e=T_E, wall_layers=WALL):
    """All parts of the ground-floor envelope [W] as a dict (keys: wall, window_east, window_south, floor, ceiling, total)."""
    parts = dict(wall=wall_load(t_i, t_e, wall_layers), window_east=window_load("east", t_i, t_e),
                 window_south=window_load("south", t_i, t_e), floor=floor_load(t_i), ceiling=ceiling_load(t_i, t_i))
    parts["total"] = sum(parts.values())
    return parts


def electricity_kwh(power_w, hours=1.0, efficiency=1.0):
    """Energy of an electric radiator that must deliver power_w for `hours` [kWh]."""
    return power_w * hours / 1000 / efficiency


# ---------------------------------------------------------------- Q3, Q4: insulation and materials
def insulation_sweep(thicknesses_m, t_i=T_I, t_e=T_E):
    """Q3: k, wall flux, total load and one-hour electricity for different EPS thicknesses."""
    rows = []
    for d in thicknesses_m:
        layers = with_insulation(WALL, "polystyrene EPS", d)
        load = total_load(t_i, t_e, layers)["total"]
        rows.append((d, k_value(layers, ALPHA_I_WALL, ALPHA_E), wall_flux(t_i, t_e, layers), load, electricity_kwh(load)))
    return pd.DataFrame(rows, columns=["eps_m", "k_wall", "flux_W_m2", "load_W", "kWh_per_hour"])


def wall_options(structure=("reinforced concrete", "solid brick", "hollow brick", "AAC"),
                 insulation=("mineral wool", "polystyrene EPS", "polystyrene XPS"),
                 d_structure=0.25, d_insulation=0.10, d_plaster=0.005, t_i=T_I, t_e=T_E):
    """Q4: every structure x insulation combination (cement plaster on both sides). Sorted by k, best first."""
    rows = []
    lam = MATERIALS
    for s in structure:
        for ins in insulation:
            layers = [("cement plaster", d_plaster, lam["cement plaster"]), (ins, d_insulation, lam[ins]),
                      (s, d_structure, lam[s]), ("cement plaster", d_plaster, lam["cement plaster"])]
            k = k_value(layers, ALPHA_I_WALL, ALPHA_E)
            thick = d_structure + d_insulation + 2 * d_plaster
            rows.append((s, ins, thick, k, k * (t_i - t_e)))
    return pd.DataFrame(rows, columns=["structure", "insulation", "thickness_m", "k_wall", "flux_W_m2"]).sort_values("k_wall").reset_index(drop=True)


# ---------------------------------------------------------------- human-centred setpoint (Q5 to Q9)
def pmv(ta, tmr, v=0.1, rh=40, clo=1.0, met=1.2):
    return calculate_pmv_ppd(ta, tmr, v, rh, clo, met)[0]


def optimal_setpoint(clo=1.0, met=1.2, rh=40, v=0.1, tmr_offset=-2.0, limit=-0.5):
    """Lowest indoor air temperature with PMV >= limit when t_mr = t_a + tmr_offset (sheet: t_a - 2)."""
    return brentq(lambda ta: pmv(ta, ta + tmr_offset, v, rh, clo, met) - limit, 5, 35)


def savings(t_i_opt, t_i=T_I, t_e=T_E):
    """Q8: load and one-hour electricity at the fixed and at the optimal setpoint, and the saving."""
    base, opt = total_load(t_i, t_e)["total"], total_load(t_i_opt, t_e)["total"]
    return dict(load_fixed=base, load_opt=opt, kwh_fixed=electricity_kwh(base), kwh_opt=electricity_kwh(opt),
                saving_W=base - opt, saving_pct=100 * (base - opt) / base)
