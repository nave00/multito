"""Implementation of a hollow cylindrical conductor topology.

This module defines :class:`HollowTopology`, representing an annular cross
section with outer and inner diameters. It computes the cross-sectional
area and returns relevant metrics for optimization.
"""

from ..core.base import Topology, TopologyRegistry


class HollowTopology(Topology):
    """Hollow cylindrical conductor topology."""

    name: str = "hollow"

    # Default design variables; can be overridden by parameters passed to evaluate
    design_variables = {
        "outer_diameter": 1.0,
        "inner_diameter": 0.5,
    }

    def evaluate(self, parameters):
        """
        Compute geometric metrics for a hollow cylindrical conductor.

        Parameters
        ----------
        parameters:
            Mapping of design variable names to their values. Any missing
            variable will fall back to the class defaults.

        Returns
        -------
        metrics:
            Dictionary containing the outer diameter, inner diameter, and
            cross-sectional area of the annulus.
        """
        outer = float(parameters.get("outer_diameter", self.design_variables["outer_diameter"]))
        inner = float(parameters.get("inner_diameter", self.design_variables["inner_diameter"]))

        # ensure inner diameter does not exceed outer; if invalid, return empty metrics
        if inner >= outer or inner <= 0.0:
            return {
                "outer_diameter": outer,
                "inner_diameter": inner,
                "area_annulus": 0.0,
            }

        from math import pi
        area_annulus = (pi / 4.0) * (outer ** 2 - inner ** 2)

        return {
            "outer_diameter": outer,
            "inner_diameter": inner,
            "area_annulus": area_annulus,
        }


# Register this topology in the registry
TopologyRegistry.register(HollowTopology)
