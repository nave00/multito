from dataclasses import dataclass
from typing import Callable, Dict, Tuple, Optional
import random

from ..core.base import Problem, Solution


@dataclass
class RandomSearchOptimizer:
    """Simple random search optimizer to find an approximate optimum within given bounds.

    Attributes:
        num_iterations: Number of random samples to evaluate.
    """
    num_iterations: int = 1000

    def optimize(
        self,
        problem: Problem,
        bounds: Dict[str, Tuple[float, float]],
        objective_func: Optional[Callable[[Dict[str, float]], float]] = None,
    ) -> Solution:
        """Optimize a topology design using random search.

        Args:
            problem: The Problem instance containing the topology to optimize.
            bounds: Dictionary mapping design variable names to a (min, max) range.
            objective_func: Optional custom objective function that takes design variables and returns a cost.
                            If None, uses problem.topology.objective.

        Returns:
            Solution with the best-found design variables and objective value. If no feasible design is found,
            returns a Solution with infinite objective value.
        """
        best_design: Optional[Dict[str, float]] = None
        best_cost: Optional[float] = None
        for _ in range(self.num_iterations):
            # Generate random design within bounds
            design = {var: random.uniform(low, high) for var, (low, high) in bounds.items()}

            # Compute cost using either custom objective or topology's objective
            cost = objective_func(design) if objective_func else problem.topology.objective(design)

            # Check feasibility
            if not problem.topology.feasibility(design):
                continue

            if best_cost is None or cost < best_cost:
                best_cost = cost
                best_design = design

        # Return a default infeasible solution if no feasible design was found
        if best_design is None or best_cost is None:
            return Solution(design_variables={}, objective_value=float("inf"))

        return Solution(design_variables=best_design, objective_value=best_cost)
