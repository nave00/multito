"""Implementation of a Litz wire conductor topology.

This module defines :class:`LitzTopology`, representing a bundle of thin strands
to reduce skin effect. It computes the total cross-sectional area and returns
metrics for optimization.
"""

from ..core.base import Topology, TopologyRegistry
from math import pi


class LitzTopology(Topology):
    """Litz wire conductor topology."""

    name: str = "litz"

    # Default design variables; can be overridden by parameters passed to evaluate
    design_variables = {
        "strand_count": 10,
        "strand_diameter": 0.1,
    }

    def evaluate(self, parameters):
        """
        Compute geometric metrics for a Litz wire conductor.

        Parameters
        ----------
        parameters:
            Mapping of design variable names to their values. Any missing
            variable will fall back to the class defaults.

        Returns
        -------
        metrics:
            Dictionary containing the strand count, strand diameter, and total
            cross-sectional area of all strands combined.
        """
        count = float(parameters.get("strand_count", self.design_variables["strand_count"]))
        diameter = float(parameters.get("strand_diameter", self.design_variables["strand_diameter"]))

        # ensure positive count and diameter
        if count <= 0 or diameter <= 0.0:
            return {
                "strand_count": count,
                "strand_diameter": diameter,
                "total_area": 0.0,
            }

        # cross-sectional area of a single strand: pi/4 * d^2
        strand_area = (pi / 4.0) * (diameter ** 2)
        total_area = count * strand_area

        return {
            "strand_count": count,
            "strand_diameter": diameter,
            "total_area": total_area,
        }


# Register this topology in the registry
TopologyRegistry.register(LitzTopology)
