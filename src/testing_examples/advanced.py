"""Funktionen mit Listen.

Listen haben zwei Dimensionen: ihre Struktur (leer, ein Element, zwei, viele) und ihre Werte.
"""


def find_max(arr: list[float]) -> float | None:
    """Findet den größten Wert einer Liste.

    Die Liste darf kein nan enthalten.

    Returns:
        den größten Wert, None für eine leere Liste

    Examples:
        >>> find_max([3.0, 1.0, 4.0, 1.0, 5.0])
        5.0
        >>> find_max([]) is None
        True
    """
    if not arr:
        return None

    max_val = arr[0]
    for val in arr[1:]:
        if val > max_val:
            max_val = val

    return max_val


def moving_average(values: list[float], window: int) -> list[float]:
    """Berechnet den gleitenden Mittelwert über je window aufeinanderfolgende Werte.

    Das Ergebnis hat len(values) - window + 1 Einträge.

    Raises:
        ValueError: wenn window kleiner als 1 oder größer als len(values) ist

    Examples:
        >>> moving_average([1.0, 2.0, 3.0, 4.0], 2)
        [1.5, 2.5, 3.5]
        >>> moving_average([1.0, 2.0, 3.0, 4.0], 1)
        [1.0, 2.0, 3.0, 4.0]
    """
    if window < 1 or window >= len(values):
        raise ValueError(f"window must be between 1 and {len(values)}, got {window}")

    return [sum(values[i : i + window]) / window for i in range(len(values) - window + 1)]
