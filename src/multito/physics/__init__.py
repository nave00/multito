"""Physics models and simulations for electrical machine optimization."""

from .losses import dc_resistance, dc_loss, skin_depth, ac_resistance, ac_loss

__all__ = [
    "dc_resistance",
    "dc_loss",
    "skin_depth",
    "ac_resistance",
    "ac_loss",
]
