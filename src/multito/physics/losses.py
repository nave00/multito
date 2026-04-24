"""Physics module providing basic electrical loss calculations for conductors."""

import math
from typing import Tuple


def dc_resistance(length: float, area: float, resistivity: float) -> float:
    """Compute DC resistance of a conductor.

    Args:
        length: Length of the conductor (meters).
        area: Cross-sectional area of the conductor (square meters).
        resistivity: Material resistivity (ohm-meter).

    Returns:
        The DC resistance in ohms.
    """
    return resistivity * length / area


def dc_loss(current: float, resistance: float) -> float:
    """Compute DC power loss in a conductor.

    Args:
        current: Current through the conductor (amperes).
        resistance: Resistance of the conductor (ohms).

    Returns:
        Power loss due to resistance in watts.
    """
    return (current ** 2) * resistance


def skin_depth(frequency: float, permeability: float, resistivity: float) -> float:
    """Compute the skin depth for a conductor at a given frequency.

    Args:
        frequency: Frequency of the current (hertz).
        permeability: Magnetic permeability of the material (henries per meter).
        resistivity: Resistivity of the material (ohm-meter).

    Returns:
        Skin depth in meters.
    """
    omega = 2 * math.pi * frequency
    return math.sqrt(2 * resistivity / (omega * permeability))


def ac_resistance(
    length: float,
    area: float,
    resistivity: float,
    frequency: float,
    permeability: float,
) -> float:
    """Approximate AC resistance using skin depth effect.

    If the skin depth is larger than the conductor radius, falls back to DC resistance.

    Args:
        length: Length of the conductor (meters).
        area: Cross-sectional area (square meters).
        resistivity: Material resistivity (ohm-meter).
        frequency: Frequency of the current (hertz).
        permeability: Magnetic permeability (henries per meter).

    Returns:
        Approximate AC resistance (ohms).
    """
    r_dc = dc_resistance(length, area, resistivity)
    radius = math.sqrt(area / math.pi)
    delta = skin_depth(frequency, permeability, resistivity)
    if delta >= radius:
        return r_dc
    # Effective area is circumference times skin depth
    effective_area = 2 * math.pi * radius * delta
    return resistivity * length / effective_area


def ac_loss(current: float, ac_resistance_value: float) -> float:
    """Compute AC power loss for a conductor.

    Args:
        current: RMS current through the conductor (amperes).
        ac_resistance_value: AC resistance (ohms).

    Returns:
        Power loss in watts.
    """
    return (current ** 2) * ac_resistance_value
