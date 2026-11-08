import pytest

import heat_loss as h


def test_existing_wall_numbers_are_unchanged():
    assert h.k_value(h.WALL, h.ALPHA_I_WALL, h.ALPHA_E) == pytest.approx(0.2198, abs=1e-3)
    assert h.wall_flux() == pytest.approx(4.18, abs=0.01)


def test_conduction_and_convection_fluxes_have_the_form_flux_equals_dt_over_resistance():
    d, lam, dt = 0.10, 0.040, 10.0
    assert h.conduction_flux(lam, d, dt) == pytest.approx(dt / (d / lam))
    assert h.convection_flux(8.0, 24.0, 20.0) == pytest.approx(4.0 / h.film_resistance(8.0))


def test_film_is_a_thin_layer_of_still_air():
    assert h.film_resistance(8.0) == pytest.approx(0.125)
    assert h.film_thickness(8.0) == pytest.approx(0.00325)
    assert h.film_thickness(24.0) < h.film_thickness(8.0)          # wind thins the film
    assert h.film_thickness(8.0) / h.LAMBDA_AIR == pytest.approx(h.film_resistance(8.0))


def test_alpha_rules_of_thumb():
    assert h.alpha_forced(4.0) == pytest.approx(24.2)
    assert h.wind_for_alpha(h.alpha_forced(2.5)) == pytest.approx(2.5)
    assert h.alpha_natural(16) == pytest.approx(2 * h.alpha_natural(1))      # 16^0.25 = 2
    assert h.alpha_natural(-4) == h.alpha_natural(4)


def test_resistance_breakdown_adds_up_to_the_total():
    b = h.resistance_breakdown(h.WALL, h.ALPHA_I_WALL, h.ALPHA_E)
    assert b["total"] == pytest.approx(h.total_resistance(h.WALL, h.ALPHA_I_WALL, h.ALPHA_E))
    assert b["film_in"] + b["layers"] + b["film_out"] == pytest.approx(b["total"])
    fl = h.resistance_breakdown(h.FLOOR, h.ALPHA_I_FLOOR)
    assert fl["film_out"] == 0.0                                      # the floor ends in soil, not in air
