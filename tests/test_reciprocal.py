"""Tests für reciprocal(x): das Muster für Ihre eigenen Testdateien.

Äquivalenzklassen
    positiv          x > 0              Repräsentant 5.0     erwartet 0.2
    negativ          x < 0              Repräsentant -5.0    erwartet -0.2
    null             x == 0             Repräsentant 0.0     erwartet ZeroDivisionError

Grenzen
    um null          -1e-6 (knapp darunter), 0.0 und -0.0 (genau darauf), 1e-6 (knapp darüber)
    Extremwerte      sys.float_info.max, sys.float_info.min, 5e-324 (kleinster positiver Float)
    nicht endlich    inf (erwartet 0.0), nan (erwartet nan)
"""

import math
import sys

import pytest

from testing_examples.simple import reciprocal

INF = math.inf
FMAX = sys.float_info.max  # größter endlicher Float, etwa 1.8e308
FMIN_NORM_POS = sys.float_info.min  # kleinster positiver normalisierter Float, etwa 2.2e-308


# Äquivalenzklassen: ein Repräsentant pro Klasse


def test_reciprocal_positive():
    """Klasse positiv (Repräsentant 5.0)"""
    assert reciprocal(5.0) == pytest.approx(0.2)


def test_reciprocal_negative():
    """Klasse negativ (Repräsentant -5.0)"""
    assert reciprocal(-5.0) == pytest.approx(-0.2)


def test_reciprocal_zero_raises():
    """Klasse null (Repräsentant 0.0)"""
    with pytest.raises(ZeroDivisionError):
        reciprocal(0.0)


# Grenzen um null: knapp darunter, genau darauf, knapp darüber


@pytest.mark.parametrize(
    ("x", "expected"),
    [
        (-1e-6, -1e6),
        (1e-6, 1e6),
    ],
)
def test_reciprocal_boundary_near_zero(x: float, expected: float):
    """Grenze knapp unter und knapp über null: Floats mit Toleranz vergleichen"""
    assert reciprocal(x) == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("x", [0.0, -0.0])
def test_reciprocal_boundary_exactly_zero_raises(x: float):
    """Grenze genau null, auch für die negative Null"""
    with pytest.raises(ZeroDivisionError, match="divide by zero"):
        reciprocal(x)


# Grenzen: Extremwerte, die noch endlich sind


def test_reciprocal_boundary_max_finite_float():
    """1 / FMAX ist etwa 5.6e-309: kleiner als FMIN_NORM_POS (subnormal), aber nicht 0"""
    result = reciprocal(FMAX)
    assert result > 0
    assert result < FMIN_NORM_POS


def test_reciprocal_boundary_min_normal_float():
    """1 / FMIN_NORM_POS ist etwa 4.5e307: noch endlich"""
    result = reciprocal(FMIN_NORM_POS)
    assert math.isfinite(result)


def test_reciprocal_boundary_min_subnormal_float():
    """1 / 5e-324 ist größer als FMAX: Das Ergebnis läuft über zu inf"""
    result = reciprocal(5e-324)
    assert result == INF


# Grenzen: nicht endliche Werte


def test_reciprocal_boundary_infinity():
    """1 / inf ist exakt 0.0, darum ist == hier in Ordnung"""
    result = reciprocal(INF)
    assert result == 0.0


def test_reciprocal_boundary_nan():
    """nan pflanzt sich fort. nan == nan ist immer False, darum math.isnan"""
    result = reciprocal(math.nan)
    assert math.isnan(result)
