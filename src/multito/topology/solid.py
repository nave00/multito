"""Concrete implementation of a solid conductor topology.

This module defines :class:`SolidTopology`, representing a simple solid
rectangular conductor cross‑section. It provides default design variables and
computes basic geometric metrics such as area and aspect ratio.
"""

from ..core.base import Topology, TopologyRegistry


class SolidTopology(Topology):
    """Solid rectangular conductor topology."""

    name: str = "solid"

    # Default design variables. Users can override these when evaluating.
    design_variables = {
        "width": 1.0,
        "height": 1.0,
    }

    def evaluate(self, parameters):
        """
        Compute geometric metrics for a solid rectangular conductor.

        Parameters
        ----------
        parameters:
            Mapping of design variable names to their values. Any missing
            variable will fall back to the class defaults.

        Returns
        -------
        metrics:
            Dictionary containing computed width, height, cross‑sectional
            area, and aspect ratio.
        """
        # Retrieve parameters with defaults
        width = float(parameters.get("width", self.design_variables["width"]))
        height = float(parameters.get("height", self.design_variables["height"]))

        area = width * height
        aspect_ratio = width / height if height != 0 else float("inf")

        return {
            "width": width,
            "height": height,
            "area": area,
            "aspect_ratio": aspect_ratio,
        }


# Register this topology so it can be discovered by name
TopologyRegistry.register(SolidTopology)
