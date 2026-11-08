import numpy as np
import pytest

import psychrometrics as ps


def test_p_sat_and_t_sat_are_inverse_on_the_table():
    assert ps.p_sat(30) == pytest.approx(4247)
    assert ps.t_sat(ps.p_sat(14)) == pytest.approx(14)


def test_humidity_ratio_and_enthalpy_of_the_sheet_summer_air():
    pv = 0.60 * ps.p_sat(30)
    x = ps.humidity_ratio(pv)
    assert 1000 * x == pytest.approx(16.26, abs=0.01)
    assert ps.enthalpy(30, x) == pytest.approx(71.55, abs=0.05)


def test_dew_point_of_30c_60pct_air():
    assert float(ps.t_sat(0.60 * ps.p_sat(30))) == pytest.approx(21.4, abs=0.2)


def test_condensation_splits_what_air_carries_from_what_it_can_hold():
    x_now, x_end, drop = ps.condensation(30, 0.60, 15)
    assert x_now > x_end > 0
    assert drop == pytest.approx(x_now - x_end)
    assert ps.condensation(30, 1.0, 30)[2] == pytest.approx(0)      # already full, cooling to the same temperature: nothing to drop


def test_daily_curves_have_24_hours_and_consistent_columns():
    d = ps.daily(ps.T_SUMMER, ps.RH_SUMMER)
    assert all(len(v) == 24 for v in d.values())
    assert np.allclose(d["gap"], d["t"] - d["tdp"])
    tab = ps.day_table(ps.T_WINTER, ps.RH_WINTER)
    assert list(tab["hour (UTC)"]) == list(range(1, 25)) and len(tab) == 24
    x, h = ps.day_x_h(ps.T_WINTER, ps.RH_WINTER)
    assert np.allclose(x, ps.daily(ps.T_WINTER, ps.RH_WINTER)["x"])


def test_correlation_of_a_curve_with_itself_is_one():
    d = ps.daily(ps.T_SUMMER, ps.RH_SUMMER)
    assert ps.correlation(d, "t", "t") == pytest.approx(1.0)
    assert ps.correlation(d, "t", "RH") < 0                 # warmer afternoons are drier


def test_comfort_range_is_a_band_and_shifts_down_with_activity_and_clothing():
    lo, hi = ps.comfort_range()
    assert 0 < hi - lo < 6
    lo_w, hi_w = ps.comfort_range(i_clo=1.0, bracket=(10, 30))
    assert hi_w < hi
    lo_a, hi_a = ps.comfort_range(m_met=2.0, bracket=(5, 30))
    assert hi_a < hi


def test_factor_sensitivity_shape_and_signs():
    base = dict(t_a=30, t_mr=30.5, v=0.15, rh=60, i_clo=0.5, m_met=1.2)
    step = {"t_a +1": ("t_a", 1), "v +0.1": ("v", 0.1)}
    g = ps.factor_sensitivity(base, step)
    assert g.shape == (6, 2)
    assert g[5, 1] > 0                                       # more air speed -> more convection loss
