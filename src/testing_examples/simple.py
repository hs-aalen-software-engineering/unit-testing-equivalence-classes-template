"""Einfache Funktionen mit einem Parameter.

Für reciprocal gibt es die Tests schon: tests/test_reciprocal.py ist das Muster für Ihre eigenen Testdateien.
"""

import math


def reciprocal(x: float) -> float:
    """Berechnet den Kehrwert 1/x.

    Returns:
        1/x. Für inf ist das Ergebnis 0.0, für nan ist es nan.

    Raises:
        ZeroDivisionError: wenn x null ist (auch -0.0)

    Examples:
        >>> reciprocal(5.0)
        0.2
        >>> reciprocal(-5.0)
        -0.2
    """
    if x == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return 1.0 / x


def absolute_value(x: float) -> float:
    """Berechnet den Betrag |x|.

    Returns:
        |x|. Für -0.0 ist das Ergebnis -0.0, das gleich 0.0 ist (-0.0 == 0.0 ist True).
        Für nan ist das Ergebnis nan.

    Examples:
        >>> absolute_value(5.0)
        5.0
        >>> absolute_value(-3.0)
        3.0
    """
    if x < 0:
        return -x
    return x


def sign(x: float) -> int:
    """Bestimmt das Vorzeichen einer Zahl.

    Returns:
        1 für jede positive Zahl, -1 für jede negative Zahl, 0 für null (auch -0.0)

    Raises:
        ValueError: wenn x nan ist

    Examples:
        >>> sign(5.0)
        1
        >>> sign(-3.0)
        -1
        >>> sign(0.0)
        0
    """
    if math.isnan(x):
        raise ValueError("sign is undefined for nan")
    if abs(x) < 1e-10:
        return 0
    if x < 0:
        return -1
    return 1
