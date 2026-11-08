import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shared"))
from solar_thermal import (DOUBLE, SINGLE, WINTER, SINGLE_OWN, reduced_temperature, efficiency,
                           useful_power, crossing, better_collector, efficiency_from_power)

# (a) reduced temperature of the winter afternoon
x_w = reduced_temperature(WINTER["t_i"], WINTER["t_a"], WINTER["g_t"])
print(f"(a) x = ({WINTER['t_i']:.0f} - {WINTER['t_a']:.0f}) / {WINTER['g_t']:.0f} = {x_w:.3f} K m2/W")

# (b) efficiency of the double-glazed collector
eta_w = efficiency(DOUBLE, x_w)
print(f"(b) eta = {DOUBLE['f_r_tau_alpha']:.2f} - {DOUBLE['f_r_u_l']:.1f} * {x_w:.3f} = {eta_w:.4f}  ({eta_w * 100:.2f} %)")

# (c) useful power per m2
q_w = useful_power(DOUBLE, WINTER["g_t"], WINTER["t_i"], WINTER["t_a"])
print(f"(c) q_u = {eta_w:.4f} * {WINTER['g_t']:.0f} = {q_w:.1f} W/m2")

# (d) each collector on its own weather
x_own = reduced_temperature(SINGLE_OWN["t_i"], SINGLE_OWN["t_a"], SINGLE_OWN["g_t"])
eta_own = efficiency_from_power(SINGLE_OWN["q_u"], SINGLE_OWN["g_t"])
print(f"(d) single-glazed, own day: x = {x_own:.3f}, eta = {eta_own:.3f}, q_u = {SINGLE_OWN['q_u']:.0f} W/m2")
print(f"    double-glazed, winter day: x = {x_w:.3f}, eta = {eta_w:.3f}, q_u = {q_w:.1f} W/m2")
print(f"    intercepts: double {DOUBLE['f_r_tau_alpha']:.2f}, single {SINGLE['f_r_tau_alpha']:.2f}")
print(f"    loss term F_R*U_L*x: double {DOUBLE['f_r_u_l'] * x_w:.4f}, single {SINGLE['f_r_u_l'] * x_own:.4f}")
q_d_own = useful_power(DOUBLE, SINGLE_OWN["g_t"], SINGLE_OWN["t_i"], SINGLE_OWN["t_a"])
print(f"    double-glazed on the single-glazed day would give {q_d_own:.1f} W/m2")

# (e) both collectors on the winter afternoon
q_s = useful_power(SINGLE, WINTER["g_t"], WINTER["t_i"], WINTER["t_a"])
eta_s = efficiency(SINGLE, x_w)
print(f"(e) double-glazed: eta = {eta_w:.4f}, q_u = {q_w:.1f} W/m2")
print(f"    single-glazed: eta = {eta_s:.4f}, q_u = {q_s:.1f} W/m2")
print(f"    better: {better_collector(DOUBLE, SINGLE, x_w)['name']}  (ratio {q_w / q_s:.2f})")

# (f) crossing point of the two efficiency lines
x_c = crossing(DOUBLE, SINGLE)
eta_c = efficiency(DOUBLE, x_c)
print(f"(f) lines cross at x = {x_c:.3f} K m2/W, eta = {eta_c:.3f}")
print(f"    just below the crossing (x = {x_c - 0.01:.2f}): {better_collector(DOUBLE, SINGLE, x_c - 0.01)['name']}")
print(f"    just above the crossing (x = {x_c + 0.01:.2f}): {better_collector(DOUBLE, SINGLE, x_c + 0.01)['name']}")
print(f"    at G_T = {WINTER['g_t']:.0f} W/m2 this is a fluid {x_c * WINTER['g_t']:.0f} K above the air; "
      f"at {SINGLE_OWN['g_t']:.0f} W/m2 it is {x_c * SINGLE_OWN['g_t']:.0f} K")

# figures: efficiency lines with the operating points, and the loss/gain split of the winter afternoon
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)
x = np.linspace(0, 0.12, 200)
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x, efficiency(DOUBLE, x), color="#2a78d6", lw=2, label="double-glazed, selective coating")
ax.plot(x, efficiency(SINGLE, x), color="#eb6834", lw=2, label="single-glazed")
ax.plot(x_c, eta_c, "ko")
ax.annotate(f"crossing: x = {x_c:.2f}, η = {eta_c:.2f}", (x_c, eta_c), xytext=(0.04, 0.72), arrowprops=dict(arrowstyle="->"))
ax.plot(x_w, eta_w, "o", color="#2a78d6", ms=8)
ax.annotate("(a)-(c) winter, double-glazed", (x_w, eta_w), xytext=(0.075, 0.55), arrowprops=dict(arrowstyle="->", color="#2a78d6"), color="#2a78d6")
ax.plot(x_own, eta_own, "o", color="#eb6834", ms=8)
ax.annotate("(d) single-glazed, own day", (x_own, eta_own), xytext=(0.005, 0.33), arrowprops=dict(arrowstyle="->", color="#eb6834"), color="#eb6834")
ax.set_xlabel("x = (T_i - T_a) / G_T  [K m2/W]")
ax.set_ylabel("efficiency η [-]")
ax.set_ylim(0, 0.8)
ax.grid(alpha=0.3)
ax.legend(loc="lower left")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "efficiency-lines.png"), dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 2.6))
absorbed = DOUBLE["f_r_tau_alpha"] * WINTER["g_t"]
lost = DOUBLE["f_r_u_l"] * x_w * WINTER["g_t"]
ax.barh(0, q_w, color="#1baf7a", label=f"useful {q_w:.1f}")
ax.barh(0, lost, left=q_w, color="#d03b3b", label=f"lost to the air {lost:.1f}")
ax.barh(0, WINTER["g_t"] - absorbed, left=absorbed, color="#e0a52a", label=f"not absorbed {WINTER['g_t'] - absorbed:.1f}")
ax.set_yticks([])
ax.set_xlabel("W per m2 of collector (the whole bar is G_T = 600 W/m2)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.45), ncol=3, frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "winter-energy-split.png"), dpi=150)
plt.close(fig)
