"""Run: python test_pv_module.py   (or pytest). Checks the model against the values printed in the sheet and hand arithmetic."""
import math
from pv_module import *


def close(a, b, tol=1e-6):
    return math.isclose(a, b, rel_tol=tol)


def test_stc_reproduces_rated_power():
    assert close(cell_temperature(800.0, 20.0), NOCT)
    assert abs(module_power(G_ST, TC_ST) - PM_ST) < 0.2               # FF * U0 * Isc = 230.1 W


def test_hot_noon_is_about_80_percent():
    p = operating_point(G_NOON, TA_NOON)
    assert close(p["tc"], 58.125)
    assert 80.0 < p["percent_of_rated"] < 82.0


def test_spring_morning_by_hand():
    p = operating_point(G_MORNING, TA_MORNING)
    assert close(p["tc"], 12 + 25 / 800 * 500)
    assert close(p["i_l"], 0.5 * (8.36 + 0.0006 * 8.36 * 2.625))
    assert close(p["u0"], 36.9 - 0.0036 * 36.9 * 2.625)
    assert close(p["p_m"], 0.746 * p["u0"] * p["i_l"])


def test_split_adds_up_and_order_matters_a_little():
    s = loss_split(G_MORNING, TA_MORNING)
    for order in ("irradiance_first", "temperature_first", "average", "log"):
        assert close(sum(s[order].values()), s["drop"])
    assert s["irradiance_first"]["temperature"] < s["temperature_first"]["temperature"]


def test_arrays_work():
    import numpy as np
    assert module_power(np.array([500.0, 1000.0]), 25.0).shape == (2,)


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
    print("all pv_module tests passed")
