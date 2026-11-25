"""Funktionen mit mehreren Parametern oder Sonderfällen.

Die Klassen hängen hier nicht von der Zahl der Parameter ab, sondern davon, was der Code mit ihnen macht.
"""

import math


def reciprocal_sum(x: float, y: float, z: float) -> float:
    """Berechnet den Kehrwert der Summe: 1 / (x + y + z).

    Returns:
        1 / (x + y + z)

    Raises:
        ZeroDivisionError: wenn der Betrag der berechneten Summe x + y + z kleiner als 1e-10 ist

    Examples:
        >>> reciprocal_sum(1.0, 2.0, 1.0)
        0.25
        >>> reciprocal_sum(-1.0, -2.0, -1.0)
        -0.25
    """
    total = x + y + z
    if abs(total) < 1e-10:
        raise ZeroDivisionError("Sum is too close to zero")
    return 1.0 / total


def calculate_ray_slope(angle_degrees: float) -> float | None:
    """Berechnet die Steigung eines Strahls aus seinem Winkel.

    Der Winkel wird von der Waagerechten aus gemessen: Positive Winkel zeigen nach unten, negative nach oben.
    Ein Strahl mit 45° fällt also und hat etwa die Steigung -1.0.

    Returns:
        die Steigung, None für senkrechte Strahlen (-90° und 90°)

    Raises:
        ValueError: wenn der Winkel kleiner als -90°, größer als 90° oder nan ist

    Examples:
        calculate_ray_slope(45.0) ergibt etwa -1.0 (der Strahl fällt),
        calculate_ray_slope(-45.0) etwa 1.0 (er steigt), calculate_ray_slope(90.0) ergibt None.
    """
    if not -90 <= angle_degrees <= 90:
        raise ValueError(f"Angle must be between -90 and 90 degrees, got {angle_degrees}")

    # Senkrechter Strahl: Es gibt keine Steigung
    if abs(angle_degrees) == 90:
        return None

    # Minus, weil positive Winkel nach unten zeigen, die y-Achse aber nach oben
    angle_rad = -math.radians(angle_degrees)
    return math.tan(angle_rad)


def triangle_type(a: float, b: float, c: float) -> str:
    """Bestimmt die Art eines Dreiecks aus seinen drei Seitenlängen.

    Drei Seiten bilden nur dann ein Dreieck, wenn jede Summe zweier Seiten größer als die dritte Seite ist.

    Returns:
        "equilateral" (alle Seiten gleich lang), "isosceles" (genau zwei gleich lang),
        "scalene" (alle verschieden lang) oder "invalid" (kein Dreieck)

    Raises:
        ValueError: wenn eine Seite null, negativ oder nicht endlich (inf, nan) ist

    Examples:
        >>> triangle_type(3.0, 3.0, 3.0)
        'equilateral'
        >>> triangle_type(3.0, 4.0, 5.0)
        'scalene'
        >>> triangle_type(1.0, 2.0, 10.0)
        'invalid'
    """
    if not all(0 < side < math.inf for side in (a, b, c)):
        raise ValueError("All side lengths must be positive and finite")

    if a + b < c or a + c < b or b + c < a:
        return "invalid"

    if a == b and b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"
