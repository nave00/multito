"""Topology definitions for different machine winding structures."""
# Import topology classes to ensure they are registered when this package is imported
from .solid import SolidTopology
from .hollow import HollowTopology
from .litz import LitzTopology

__all__ = [
    "SolidTopology",
    "HollowTopology",
    "LitzTopology",
]
