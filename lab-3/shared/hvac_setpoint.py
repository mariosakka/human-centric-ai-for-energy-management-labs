"""Reusable building blocks for App 2.3 (HVAC setpoint). Every function only returns values: no printing, no plots."""
import numpy as np
import pandas as pd
from scipy.optimize import brentq

from calculate_pmv_ppd import calculate_pmv_ppd

LIMIT = 0.5   # Category II: -0.5 < PMV < 0.5


def pmv(ta, tmr, v=0.1, rh=50, clo=0.5, met=1.2):
    """PMV only."""
    return calculate_pmv_ppd(ta, tmr, v, rh, clo, met)[0]


def ppd(ta, tmr, v=0.1, rh=50, clo=0.5, met=1.2):
    """PPD only [%]."""
    return calculate_pmv_ppd(ta, tmr, v, rh, clo, met)[1]


def ta_for_pmv(target, tmr, v=0.1, rh=50, clo=0.5, met=1.2, lo=5, hi=40):
    """Air temperature that gives PMV == target. tmr is a number or a function ta -> tmr."""
    t_mr = tmr if callable(tmr) else (lambda ta: tmr)
    return brentq(lambda ta: pmv(ta, t_mr(ta), v, rh, clo, met) - target, lo, hi)


def lowest_setpoint(tmr, v=0.1, rh=40, clo=1.0, met=1.2):
    """Lowest ta with PMV >= -0.5 (Part 3, root finder)."""
    return ta_for_pmv(-LIMIT, tmr, v, rh, clo, met)


def highest_setpoint(tmr, v=0.1, rh=50, clo=0.5, met=1.2):
    """Highest ta with PMV <= +0.5."""
    return ta_for_pmv(LIMIT, tmr, v, rh, clo, met)


def lowest_setpoint_while(tmr, v=0.1, rh=40, clo=1.0, met=1.2, step=0.05, start=10.0):
    """Same as lowest_setpoint with a plain while loop, like a simple controller. Returns (ta, n_steps)."""
    ta, n = start, 0
    while pmv(ta, tmr, v, rh, clo, met) < -LIMIT:
        ta += step
        n += 1
    return ta, n


def fan_sensitivity(ta0=25.0, v0=0.1, speeds=None, rh=50, clo=0.5, met=1.2, dtmr=1.0):
    """Part 1. For each air speed: ta giving the same PMV as (ta0, v0), the gain, and the upper comfort limit."""
    speeds = np.round(np.arange(0.1, 0.81, 0.1), 1) if speeds is None else speeds
    ref = pmv(ta0, ta0 + dtmr, v0, rh, clo, met)
    rows = []
    for v in speeds:
        same = ta_for_pmv(ref, lambda t: t + dtmr, v, rh, clo, met)
        limit = ta_for_pmv(LIMIT, lambda t: t + dtmr, v, rh, clo, met)
        rows.append((v, same, same - ta0, limit, pmv(ta0, ta0 + dtmr, v, rh, clo, met)))
    out = pd.DataFrame(rows, columns=["v", "ta_same_pmv", "gain", "ta_at_limit", "pmv_if_ta_unchanged"])
    out.attrs["pmv_ref"] = ref
    return out


def load_day(path):
    """24 h CSV -> DataFrame with columns hour, ta, tmr, rh."""
    df = pd.read_csv(path)
    df.columns = ["hour", "ta", "tmr", "rh"]
    return df


def free_running_day(df, clo=0.7, met=1.2, v=0.1):
    """Part 2. Add pmv, ppd, t_o and status ('too cold' / 'ok' / 'too warm') to every row of the day."""
    res = [calculate_pmv_ppd(r.ta, r.tmr, v, r.rh, clo, met) for r in df.itertuples()]
    out = df.copy()
    out["pmv"] = [r[0] for r in res]
    out["ppd"] = [r[1] for r in res]
    out["t_o"] = [r[2] for r in res]
    out["status"] = np.where(out.pmv <= -LIMIT, "too cold", np.where(out.pmv >= LIMIT, "too warm", "ok"))
    return out


def hours_outside(day):
    """Hours of a free_running_day table that are outside comfort: (cold_hours, warm_hours)."""
    return list(day.hour[day.status == "too cold"]), list(day.hour[day.status == "too warm"])


def setpoint_vs_tmr(tmrs, v=0.1, rh=40, clo=1.0, met=1.2, clo_light=None):
    """Part 3 extra. Lowest ta for each mean radiant temperature, for clo and for a lighter clo (default clo - 0.2)."""
    clo_light = clo - 0.2 if clo_light is None else clo_light
    return pd.DataFrame({
        "tmr": list(tmrs),
        "ta_min": [lowest_setpoint(t, v, rh, clo, met) for t in tmrs],
        "ta_min_light": [lowest_setpoint(t, v, rh, clo_light, met) for t in tmrs],
    })


# Part 4: seasonal presets. tmr is a function ta -> tmr.
SEASONS = {
    "summer":        dict(clo=0.5, met=1.2, rh=50, v=0.1, tmr=lambda ta: ta + 1),
    "autumn/spring": dict(clo=0.7, met=1.2, rh=50, v=0.1, tmr=lambda ta: ta),
    "winter":        dict(clo=1.0, met=1.2, rh=40, v=0.1, tmr=lambda ta: 17.0),
    "winter, heavy": dict(clo=1.2, met=1.2, rh=40, v=0.1, tmr=lambda ta: 16.0),
}


def comfort_band(clo, met, rh, v, tmr):
    """(lowest, highest) ta with -0.5 <= PMV <= 0.5. tmr is a number or a function ta -> tmr."""
    return (ta_for_pmv(-LIMIT, tmr, v, rh, clo, met), ta_for_pmv(LIMIT, tmr, v, rh, clo, met))


def seasons_table(df, seasons=None):
    """Part 4. Comfort band per season plus the hours of the day (df) outside comfort with that clothing."""
    rows = []
    for name, s in (SEASONS if seasons is None else seasons).items():
        lo, hi = comfort_band(**s)
        day = free_running_day(df, s["clo"], s["met"], s["v"])
        # use the season's rh only for the band; the day keeps its own rh column
        rows.append((name, lo, hi, hi - lo, int((day.status != "ok").sum()), day.pmv.min(), day.pmv.max()))
    return pd.DataFrame(rows, columns=["season", "ta_min", "ta_max", "width", "hours_outside", "pmv_min", "pmv_max"])
