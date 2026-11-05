"""Checks against the sheet: python -m pytest lab-5/shared"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from math import isclose
from solar_thermal import *


def test_double_glazed_winter():
    x = reduced_temperature(**{k: WINTER[k] for k in ("t_i", "t_a", "g_t")})
    assert isclose(x, 0.075)
    assert isclose(efficiency(DOUBLE, x), 0.4375)
    assert isclose(useful_power(DOUBLE, **WINTER), 262.5)


def test_single_glazed_own_day_matches_sheet():
    q = useful_power(SINGLE, SINGLE_OWN["g_t"], SINGLE_OWN["t_i"], SINGLE_OWN["t_a"])
    assert abs(q - SINGLE_OWN["q_u"]) < 1.0           # the sheet rounds to 412 W/m2


def test_same_winter_day_double_wins():
    assert isclose(useful_power(SINGLE, **WINTER), 180.0)
    assert better_collector(DOUBLE, SINGLE, 0.075) is DOUBLE


def test_crossing():
    x = crossing(DOUBLE, SINGLE)
    assert isclose(x, 0.02)
    assert isclose(efficiency(DOUBLE, x), efficiency(SINGLE, x))
    assert better_collector(DOUBLE, SINGLE, 0.01) is SINGLE
    assert better_collector(DOUBLE, SINGLE, 0.03) is DOUBLE
    assert crossing(DOUBLE, dict(DOUBLE)) is None
