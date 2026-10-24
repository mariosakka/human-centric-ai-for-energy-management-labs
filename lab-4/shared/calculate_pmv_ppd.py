"""PMV / PPD / operative temperature (ISO 7730, Fanger). Pure function: returns values, never prints."""
import math


def calculate_pmv_ppd(t_a, t_mr, v=0.15, rh=60, i_clo=0.5, m_met=1.2):
    """Return (pmv, ppd, t_o, n_iterations). Temperatures in C, v in m/s, rh in %."""
    M = m_met * 58.15                                     # W/m2
    I_cl = 0.155 * i_clo                                  # m2K/W
    p_sat = math.exp(16.6536 - 4030.183 / (t_a + 235))    # kPa
    p_v = rh / 100 * p_sat * 1000                         # Pa
    f_cl = 1 + 1.29 * I_cl if I_cl < 0.078 else 1.05 + 0.645 * I_cl

    # iterate clothing surface temperature
    T_a = t_a + 273.15
    T_mr = t_mr + 273.15
    h_cf = 12.1 * math.sqrt(v)
    p1 = I_cl * f_cl
    p2 = p1 * 3.96
    p3 = p1 * 100
    p4 = p1 * T_a
    p5 = 308.7 - 0.028 * M + p2 * (T_mr / 100) ** 4
    T_cl = T_a + (35.5 - t_a) / (3.5 * I_cl + 0.1)        # initial estimate
    xn = T_cl / 100
    xf = T_cl / 50
    n = 0
    while abs(xn - xf) > 0.0015:
        xf = (xf + xn) / 2
        h_cn = 2.38 * abs(100 * xf - T_a) ** 0.25
        h_c = max(h_cf, h_cn)
        xn = (p5 + p4 * h_c - p2 * xf ** 4) / (100 + p3 * h_c)
        n += 1
    t_cl = 100 * xn - 273.15

    # heat losses
    HL1 = 3.05e-3 * (5733 - 6.99 * M - p_v)
    HL2 = 0.42 * (M - 58.15) if M > 58.15 else 0
    HL3 = 1.7e-5 * M * (5867 - p_v)
    HL4 = 0.0014 * M * (34 - t_a)
    HL5 = 3.96 * f_cl * (xn ** 4 - (T_mr / 100) ** 4)
    HL6 = f_cl * h_c * (t_cl - t_a)

    # PMV and PPD
    TS = 0.303 * math.exp(-0.036 * M) + 0.028
    pmv = TS * (M - HL1 - HL2 - HL3 - HL4 - HL5 - HL6)
    ppd = 100 - 95 * math.exp(-0.03353 * pmv ** 4 - 0.2179 * pmv ** 2)

    # operative temperature
    if v < 0.2:
        t_o = 0.5 * t_a + 0.5 * t_mr
    elif v < 0.6:
        t_o = 0.6 * t_a + 0.4 * t_mr
    else:
        t_o = 0.7 * t_a + 0.3 * t_mr
    return pmv, ppd, t_o, n


def show(t_a, t_mr, v=0.15, rh=60, i_clo=0.5, m_met=1.2):
    """Print in the lab-sheet format and return the same tuple."""
    pmv, ppd, t_o, n = calculate_pmv_ppd(t_a, t_mr, v, rh, i_clo, m_met)
    print('PMV=', round(pmv, 3), 'PPD=', round(ppd, 1), 't_o=', round(t_o, 2), 'n iterations=', n)
    return pmv, ppd, t_o, n


if __name__ == '__main__':
    print('Exterior air (summer day in Romania):')
    show(t_a=30, t_mr=30.5, v=0.15, rh=60, i_clo=0.5, m_met=1.2)
    print('Interior air conditions:')
    show(t_a=25, t_mr=25.5, v=0.15, rh=50, i_clo=0.5, m_met=1.2)
