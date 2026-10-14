import math


def calculate_pmv_ppd(t_a, t_mr, v=0.15, rh=60, i_clo=0.5, m_met=1.2):
    """Return PMV, PPD, operative temperature and number of iterations."""
    # step 2: unit conversions
    m = m_met * 58.15
    icl = i_clo * 0.155
    vapor_pressure = (rh / 100) * math.exp(16.6536 - 4030.183 / (t_a + 235)) * 1000  # kPa -> Pa

    if icl < 0.078:
        f_cl = 1 + 1.29 * icl
    else:
        f_cl = 1.05 + 0.645 * icl

    # step 3: clothing temperature, found by iteration
    air_k = t_a + 273.15
    radiant_k = t_mr + 273.15
    t_cl = air_k + (35.5 - t_a) / (3.5 * (6.45 * icl + 0.1))  # first guess (ISO 7730)
    forced_h = 12.1 * math.sqrt(v)

    # this form is from ISO 7730
    p1 = icl * f_cl
    p2 = p1 * 3.96
    p3 = p1 * 100
    p4 = p1 * air_k
    p5 = 308.7 - 0.028 * m + p2 * (radiant_k / 100) ** 4

    x = t_cl / 100
    old_x = 2 * x
    iterations = 0

    while abs(x - old_x) > 0.0015:
        old_x = (old_x + x) / 2
        clothing_c = 100 * old_x - 273.15
        natural_h = 2.38 * abs(clothing_c - t_a) ** 0.25
        h_c = max(forced_h, natural_h)
        x = (p5 + p4 * h_c - p2 * old_x ** 4) / (100 + p3 * h_c)
        iterations += 1
        if iterations > 150:
            raise RuntimeError("Clothing temperature did not converge")

    clothing_c = 100 * x - 273.15

    # step 4: the six heat losses
    loss_skin = 3.05e-3 * (5733 - 6.99 * m - vapor_pressure)
    loss_sweat = 0.42 * max(m - 58.15, 0)
    loss_breath_moisture = 1.7e-5 * m * (5867 - vapor_pressure)
    loss_breath_heat = 0.0014 * m * (34 - t_a)
    loss_radiation = 3.96 * f_cl * ((x ** 4) - (radiant_k / 100) ** 4)
    loss_convection = f_cl * h_c * (clothing_c - t_a)

    # step 5: PMV and PPD
    heat_left = m - (loss_skin + loss_sweat + loss_breath_moisture
                     + loss_breath_heat + loss_radiation + loss_convection)
    pmv = (0.303 * math.exp(-0.036 * m) + 0.028) * heat_left
    ppd = 100 - 95 * math.exp(-0.03353 * pmv ** 4 - 0.2179 * pmv ** 2)

    # step 6: operative temperature
    if v < 0.2:
        t_o = 0.5 * t_a + 0.5 * t_mr
    elif v < 0.6:
        t_o = 0.6 * t_a + 0.4 * t_mr
    else:
        t_o = 0.7 * t_a + 0.3 * t_mr

    return pmv, ppd, t_o, iterations


def print_results(label, t_a, t_mr, v=0.15, rh=60, i_clo=0.5, m_met=1.2):
    pmv, ppd, t_o, iterations = calculate_pmv_ppd(t_a, t_mr, v, rh, i_clo, m_met)
    print(f"\n{label}")
    print("Inputs:")
    print(f"  t_a= {t_a} °C")
    print(f"  t_mr= {t_mr} °C")
    print(f"  RH= {rh} %")
    print(f"  v= {v} m/s")
    print(f"  clo= {i_clo}")
    print(f"  M_met= {m_met} met")
    print("Outputs:")
    print(f"  PMV= {pmv:.3f}")
    print(f"  PPD= {ppd:.1f} %")
    print(f"  t_o= {t_o:.2f} °C")
    print(f"  n iterations= {iterations}")
    return pmv


if __name__ == "__main__":
    print_results("Outside - summer day", 30, 30.5)
    indoor_pmv = print_results("Inside - comfortable room", 24.5, 25)

    if -0.5 < indoor_pmv < 0.5:
        print("\nIndoor conditions meet the comfort requirement.")
    else:
        print("\nIndoor conditions need adjustment.")
