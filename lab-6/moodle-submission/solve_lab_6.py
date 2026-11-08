"""Lab 6 - Solar to electric energy conversion (Kyocera KD230GX-LPB). Prints the answers (a) to (e) and saves two figures.
Run:  conda run -n human-centric-ai-for-energy-labs python lab-6/moodle-submission/solve_lab_6.py
All formulas are in ../shared/pv_module.py; this file only calls them."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shared"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pv_module import (G_MORNING, TA_MORNING, G_NOON, TA_NOON, PM_ST,
                       operating_point, loss_split, relative_efficiency)

# --- (a)
m = operating_point(G_MORNING, TA_MORNING)
print(f"(a) tc = {m['tc']:.2f} C   (air {m['ta']:.0f} C + {m['tc'] - m['ta']:.2f} K of heating by the sun)")

# --- (b)
print(f"(b) I_L = Isc = {m['i_l']:.3f} A   U0 = {m['u0']:.2f} V")

# --- (c)
print(f"(c) P_M = {m['p_m']:.1f} W")

# --- (d)
noon = operating_point(G_NOON, TA_NOON)
print(f"(d) spring morning: P_M = {m['p_m']:.1f} W = {m['percent_of_rated']:.1f} % of {PM_ST:.0f} W")
print(f"    hot noon:       tc = {noon['tc']:.1f} C, P_M = {noon['p_m']:.1f} W = {noon['percent_of_rated']:.1f} %")
print(f"    output per unit of sunlight, STC = 100 %: morning {relative_efficiency(G_MORNING, m['tc']):.1f} %,"
      f" noon {relative_efficiency(G_NOON, noon['tc']):.1f} %")

# --- (e)
split = loss_split(G_MORNING, TA_MORNING)
print(f"(e) drop from {split['p_stc']:.1f} W to {split['p_m']:.1f} W = {split['drop']:.1f} W")
for key, label in (("irradiance_first", "irradiance first"), ("temperature_first", "temperature first"),
                   ("average", "average of both"), ("log", "logarithmic (no order)")):
    s = split[key]
    print(f"    {label:<22} irradiance {s['irradiance']:6.1f} W   cell temperature {s['temperature']:5.1f} W")
split_noon = loss_split(G_NOON, TA_NOON)
print(f"    hot noon, average of both: irradiance {split_noon['average']['irradiance']:.1f} W,"
      f" cell temperature {split_noon['average']['temperature']:.1f} W")

# --- figures (drawing only)
os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8a85"

fig, ax = plt.subplots(figsize=(6.4, 3.2))
steps = [("STC\n1000 W/m2, 25 C", split["p_stc"]), ("lower sunlight only\n500 W/m2, 25 C", split["p_stc"] - split["irradiance_first"]["irradiance"]),
         ("spring morning\n500 W/m2, 27.6 C", split["p_m"])]
bars = ax.bar([s[0] for s in steps], [s[1] for s in steps], color=[GREY, BLUE, ORANGE], width=0.55)
for b, (_, v) in zip(bars, steps):
    ax.text(b.get_x() + b.get_width() / 2, v + 4, f"{v:.1f} W", ha="center", fontsize=9)
ax.set_ylabel("module power P_M [W]"); ax.set_ylim(0, 270)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
plt.tight_layout(); plt.savefig(os.path.join(HERE, "figures", "power-steps.png"), dpi=170); plt.close()

fig, ax = plt.subplots(figsize=(6.4, 3.4))
cases = [("spring morning\n500 W/m2, 12 C", split["average"]), ("hot noon\n900 W/m2, 30 C", split_noon["average"])]
for y, (name, s) in enumerate(cases):
    ax.barh(y, s["irradiance"], color=BLUE, label="lower irradiance" if y == 0 else None)
    ax.barh(y, s["temperature"], left=s["irradiance"], color=ORANGE, label="hotter cell" if y == 0 else None)
    ax.text(s["irradiance"] + s["temperature"] + 2, y, f"{s['irradiance']:.0f} W + {s['temperature']:.0f} W", va="center", fontsize=9)
ax.set_yticks([0, 1]); ax.set_yticklabels([c[0] for c in cases]); ax.set_xlim(0, 160)
ax.set_xlabel("power lost compared with 230 W [W] (average of both orders)"); ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=2)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
plt.tight_layout(); plt.savefig(os.path.join(HERE, "figures", "loss-split.png"), dpi=170); plt.close()
