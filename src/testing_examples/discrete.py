"""Funktionen mit wenigen möglichen Ergebnissen.

Die Rückgabewerte stehen fest. Die Grenzen liegen bei den Schwellenwerten, an denen das Ergebnis wechselt.
"""

import math


def calculate_grade(score: float) -> str:
    """Wandelt eine Punktzahl in eine Note um.

    Notenskala:
        "A": 90 <= score <= 100
        "B": 80 <= score < 90
        "C": 70 <= score < 80
        "D": 60 <= score < 70
        "F":  0 <= score < 60

    Raises:
        ValueError: wenn score kleiner als 0, größer als 100 oder nan ist

    Examples:
        >>> calculate_grade(95.0)
        'A'
        >>> calculate_grade(50.0)
        'F'
    """
    if not 0 <= score <= 100:
        raise ValueError(f"Score must be between 0 and 100, got {score}")
    if score >= 90:
        return "A"
    if score > 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def classify_temperature(temp_celsius: float) -> str:
    """Ordnet eine Temperatur in Grad Celsius einer Kategorie zu.

    Kategorien:
        "freezing":       temp_celsius < 0
        "cold":      0 <= temp_celsius < 10
        "mild":     10 <= temp_celsius < 20
        "warm":     20 <= temp_celsius < 30
        "hot":      30 <= temp_celsius

    Raises:
        ValueError: wenn temp_celsius nan ist

    Examples:
        >>> classify_temperature(15.0)
        'mild'
        >>> classify_temperature(-5.0)
        'freezing'
    """
    if math.isnan(temp_celsius):
        raise ValueError("Temperature must not be nan")
    if temp_celsius < 0:
        return "freezing"
    if temp_celsius < 10:
        return "cold"
    if temp_celsius < 20:
        return "mild"
    if temp_celsius < 30:
        return "warm"
    return "hot"


def day_type(day: str) -> str:
    """Ordnet einen englischen Wochentag ein.

    Groß- und Kleinschreibung spielen keine Rolle. Leerzeichen werden nicht entfernt.

    Returns:
        "weekday" für monday bis friday, "weekend" für saturday und sunday, "invalid" für alles andere

    Examples:
        >>> day_type("Monday")
        'weekday'
        >>> day_type("saturday")
        'weekend'
        >>> day_type("Montag")
        'invalid'
    """
    day_lower = day.lower()

    weekdays = {"monday", "tuesday", "wednesday", "thursday", "friday"}
    weekends = {"saturday", "sunday"}

    if day_lower in weekdays:
        return "weekday"
    if day_lower in weekends:
        return "weekend"
    return "invalid"
