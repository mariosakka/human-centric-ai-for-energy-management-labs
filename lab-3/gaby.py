# PMV, PPD and operative temperature 
import math
import pandas as pd
import matplotlib.pyplot as plt


def calculate_pmv_ppd(t_a, t_mr, v, rh, i_clo, m_met, show=True):
    # Step 2: unit conversions
    M = m_met * 58.15                       # W/m2
    I_cl = 0.155 * i_clo                    # m2K/W
    p_sat = math.exp(16.6536 - 4030.183 / (t_a + 235))   # kPa
    p_v = rh / 100 * p_sat * 1000                         # Pa
    f_cl = 1 + 1.29 * I_cl if I_cl < 0.078 else 1.05 + 0.645 * I_cl

    # Step 3: iterate clothing surface temperature
    T_a = t_a + 273.15
    T_mr = t_mr + 273.15
    h_cf = 12.1 * math.sqrt(v)
    p1 = I_cl * f_cl
    p2 = p1 * 3.96
    p3 = p1 * 100
    p4 = p1 * T_a
    p5 = 308.7 - 0.028 * M + p2 * (T_mr / 100) ** 4
    T_cl = T_a + (35.5 - t_a) / (3.5 * I_cl + 0.1)   # initial estimate
    xn = T_cl / 100
    xf = T_cl / 50
    eps = 0.0015
    n = 0
    while abs(xn - xf) > eps:
        xf = (xf + xn) / 2
        h_cn = 2.38 * abs(100 * xf - T_a) ** 0.25
        h_c = max(h_cf, h_cn)
        xn = (p5 + p4 * h_c - p2 * xf ** 4) / (100 + p3 * h_c)
        n += 1
    t_cl = 100 * xn - 273.15

    # Step 4: heat losses
    HL1 = 3.05e-3 * (5733 - 6.99 * M - p_v)
    HL2 = 0.42 * (M - 58.15) if M > 58.15 else 0
    HL3 = 1.7e-5 * M * (5867 - p_v)
    HL4 = 0.0014 * M * (34 - t_a)
    HL5 = 3.96 * f_cl * (xn ** 4 - (T_mr / 100) ** 4)
    HL6 = f_cl * h_c * (t_cl - t_a)

    # Step 5: PMV and PPD
    TS = 0.303 * math.exp(-0.036 * M) + 0.028
    L = M - HL1 - HL2 - HL3 - HL4 - HL5 - HL6
    pmv = TS * L
    ppd = 100 - 95 * math.exp(-0.03353 * pmv ** 4 - 0.2179 * pmv ** 2)

    # Step 6: operative temperature
    if v < 0.2:
        t_o = 0.5 * t_a + 0.5 * t_mr
    elif v < 0.6:
        t_o = 0.6 * t_a + 0.4 * t_mr
    else:
        t_o = 0.7 * t_a + 0.3 * t_mr

    if show:
        print('PMV=', round(pmv, 3), 'PPD=', round(ppd, 1), 't_o=', round(t_o, 2), 'n iterations=', n)
    return pmv, ppd, t_o, n


print('Exterior air (summer day in Romania):')
calculate_pmv_ppd(t_a=30, t_mr=30.5, v=0.15, rh=60, i_clo=0.5, m_met=1.2)

print('Interior air conditions:')
calculate_pmv_ppd(t_a=25, t_mr=25.5, v=0.15, rh=50, i_clo=0.5, m_met=1.2)


# Part 1: Sensitivity analysis - air velocity vs. air temperature
# Summer office: clo = 0.5, met = 1.2, RH = 50%, tmr = ta + 1
print()
print('Part 1: Sensitivity analysis (summer office)')
ta_ref = 25.0
pmv_ref = calculate_pmv_ppd(ta_ref, ta_ref + 1, 0.1, 50, 0.5, 1.2, show=False)[0]
print('Reference: ta =', ta_ref, 'C, v = 0.1 m/s -> PMV =', round(pmv_ref, 3))
print('v [m/s]   ta [C]   delta ta [C]   PMV')
v_list, ta_list = [], []
v = 0.1
while v <= 0.8 + 1e-9:
    # find ta that gives the same PMV (bisection)
    lo, hi = 15.0, 40.0
    for _ in range(50):
        ta = (lo + hi) / 2
        pmv = calculate_pmv_ppd(ta, ta + 1, v, 50, 0.5, 1.2, show=False)[0]
        if pmv < pmv_ref:
            lo = ta
        else:
            hi = ta
    print(f'{v:5.1f}    {ta:6.2f}      {round(ta - ta_ref, 2) + 0.0:+5.2f}        {pmv:.3f}')
    v_list.append(round(v, 1))
    ta_list.append(ta)
    v += 0.1


# Part 2: Dynamic data processing - 24 h meteo/building file
# v = 0.1 m/s, clo = 0.5, met = 1.2 (no HVAC)
print()
print('Part 2: Hourly comfort check (date_cladire_24h.csv)')
df = pd.read_csv('date_cladire_24h.csv')
df.columns = ['hour', 'ta', 'tmr', 'rh']
res = df.apply(lambda r: calculate_pmv_ppd(r.ta, r.tmr, 0.1, r.rh, 0.5, 1.2, show=False), axis=1)
df['PMV'] = [round(x[0], 2) for x in res]
df['PPD'] = [round(x[1], 1) for x in res]
df['comfort'] = df['PMV'].apply(lambda p: 'OK' if -0.5 < p < 0.5 else ('too cold' if p <= -0.5 else 'too warm'))
print(df.to_string(index=False))
print('Hours outside the comfort zone:', list(df.loc[df['comfort'] != 'OK', 'hour']))


# Part 3: HVAC setpoint optimization - extreme winter scenario
# cold windows -> low tmr; clo = 1.2 (winter clothing), met = 1.2, RH = 40%, v = 0.1 m/s
print()
print('Part 3: Lowest air temperature with PMV >= -0.5 (winter)')
t_mr_winter = 16.0
t_a = 16.0
pmv = calculate_pmv_ppd(t_a, t_mr_winter, 0.1, 40, 1.2, 1.2, show=False)[0]
while pmv < -0.5:
    t_a += 0.1
    pmv = calculate_pmv_ppd(t_a, t_mr_winter, 0.1, 40, 1.2, 1.2, show=False)[0]
print('tmr =', t_mr_winter, 'C -> optimal setpoint ta =', round(t_a, 1), 'C')
calculate_pmv_ppd(round(t_a, 1), t_mr_winter, 0.1, 40, 1.2, 1.2)
print('Fixed standard setpoint ta = 23 C:')
calculate_pmv_ppd(23, t_mr_winter, 0.1, 40, 1.2, 1.2)
print('Overheating avoided:', round(23 - t_a, 1), 'C')


# Plots
plt.figure()
plt.plot(v_list, ta_list, 'o-')
plt.xlabel('Air velocity v [m/s]')
plt.ylabel('Air temperature ta [C]')
plt.title('Part 1: ta for the same PMV vs. air velocity')
plt.grid(True)
plt.savefig('part1_velocity.png', dpi=120)

plt.figure()
plt.plot(df['hour'], df['PMV'], 'o-', label='PMV')
plt.axhspan(-0.5, 0.5, color='green', alpha=0.2, label='Comfort zone')
plt.xlabel('Hour')
plt.ylabel('PMV [-]')
plt.title('Part 2: Hourly PMV without HVAC')
plt.legend()
plt.grid(True)
plt.savefig('part2_hourly_pmv.png', dpi=120)

ta_range = [18 + 0.1 * i for i in range(71)]
pmv_range = [calculate_pmv_ppd(t, t_mr_winter, 0.1, 40, 1.2, 1.2, show=False)[0] for t in ta_range]
plt.figure()
plt.plot(ta_range, pmv_range, label='PMV')
plt.axhline(-0.5, color='red', linestyle='--', label='PMV = -0.5')
plt.axvline(t_a, color='green', linestyle='--', label=f'Optimal setpoint {t_a:.1f} C')
plt.axvline(23, color='gray', linestyle=':', label='Fixed setpoint 23 C')
plt.xlabel('Air temperature ta [C]')
plt.ylabel('PMV [-]')
plt.title('Part 3: HVAC setpoint optimization (winter)')
plt.legend()
plt.grid(True)
plt.savefig('part3_setpoint.png', dpi=120)
plt.show()