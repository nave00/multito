"""Hollow topology representing a rectangular or cylindrical winding with a central void."""

from dataclasses import dataclass, field
from typing import Dict

from ..core.base import Topology, TopologyRegistry


@dataclass
class HollowTopology(Topology):
    """Simple hollow topology with outer and inner diameters."""
    name: str = "hollow"
    design_vars: Dict[str, float] = field(
        default_factory=lambda: {"outer_diameter": 1.0, "inner_diameter": 0.5}
    )

    def objective(self) -> float:
        """Compute a simple objective based on area difference (outer^2 - inner^2)."""
        outer = self.design_vars.get("outer_diameter", 1.0)
        inner = self.design_vars.get("inner_diameter", 0.5)
        return outer ** 2 - inner ** 2

    def is_feasible(self) -> bool:
        """Check feasibility: outer diameter must be greater than inner diameter."""
        outer = self.design_vars.get("outer_diameter", 1.0)
        inner = self.design_vars.get("inner_diameter", 0.5)
        return outer > inner


# Register the topology in the global registry
TopologyRegistry.register("hollow", HollowTopology)
