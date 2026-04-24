"""Litz wire topology representing many thin strands for reduced skin effect losses."""

from dataclasses import dataclass, field
from typing import Dict

from ..core.base import Topology, TopologyRegistry


@dataclass
class LitzTopology(Topology):
    """Simple litz wire topology with a number of strands and strand diameter."""
    name: str = "litz"
    design_vars: Dict[str, float] = field(
        default_factory=lambda: {"strand_count": 10, "strand_diameter": 0.1}
    )

    def objective(self) -> float:
        """Compute total cross-sectional area as objective (count * diameter^2)."""
        count = self.design_vars.get("strand_count", 10)
        diameter = self.design_vars.get("strand_diameter", 0.1)
        return count * (diameter ** 2)

    def is_feasible(self) -> bool:
        """Check feasibility: both strand count and diameter must be positive."""
        count = self.design_vars.get("strand_count", 0)
        diameter = self.design_vars.get("strand_diameter", 0.0)
        return count > 0 and diameter > 0


# Register the topology
TopologyRegistry.register("litz", LitzTopology)
