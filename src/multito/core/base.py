"""Core abstractions and dataclasses for the multito package.

This module defines the base classes that represent optimization problems,
solutions, and conductor topologies. These abstractions serve as the core
contract for the rest of the library.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List, Optional, Type


class Topology:
    """
    Base class for conductor topologies.

    A topology encapsulates the design variables and provides a way to evaluate
    derived metrics (such as cross‑sectional area, winding factors, etc.).
    Concrete topologies should inherit from this class and implement
    :meth:`evaluate`.
    """

    #: Human‑readable name of the topology.
    name: str = "base"

    #: A dictionary describing the default design variables for this topology.
    design_variables: Dict[str, Any] = {}

    def evaluate(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the topology with the given design parameters.

        Parameters
        ----------
        parameters:
            A mapping of variable names to values.

        Returns
        -------
        metrics:
            A dictionary of computed metrics specific to the topology.

        Raises
        ------
        NotImplementedError
            If the topology does not provide an implementation.
        """
        raise NotImplementedError("Topology subclasses must implement evaluate().")


class TopologyRegistry:
    """
    Registry for available topologies.

    This registry enables discovery of topologies by name and supports
    extension via plugin registration. New topology classes can be added
    by calling :meth:`register`.
    """

    _registry: Dict[str, Type[Topology]] = {}

    @classmethod
    def register(cls, topology_cls: Type[Topology]) -> None:
        """Register a topology class in the registry."""
        cls._registry[topology_cls.name] = topology_cls

    @classmethod
    def get(cls, name: str) -> Type[Topology]:
        """Retrieve a topology class by its registered name."""
        if name not in cls._registry:
            raise KeyError(f"Topology '{name}' is not registered.")
        return cls._registry[name]

    @classmethod
    def all(cls) -> Dict[str, Type[Topology]]:
        """Return a copy of the internal registry."""
        return dict(cls._registry)


@dataclass
class Problem:
    """
    Representation of a multi‑objective optimization problem.

    An instance of :class:`Problem` collects all information necessary to
    perform an optimization: the design parameters, objective functions,
    constraints, and the topology under investigation.
    """

    parameters: Dict[str, Any]
    objective_functions: List[Callable[[Dict[str, Any], Topology], float]]
    constraints: List[Callable[[Dict[str, Any], Topology], bool]] = field(default_factory=list)
    topology: Optional[Topology] = None

    def evaluate_objectives(self, design_vars: Dict[str, Any]) -> List[float]:
        """
        Evaluate all objective functions using the provided design variables.

        Parameters
        ----------
        design_vars:
            A dictionary of design variable assignments.

        Returns
        -------
        objectives:
            The list of computed objective values.
        """
        if self.topology is None:
            raise ValueError("Problem has no topology assigned.")
        metrics = self.topology.evaluate(design_vars)
        return [obj(metrics, self.topology) for obj in self.objective_functions]

    def is_feasible(self, design_vars: Dict[str, Any]) -> bool:
        """
        Check whether a given design is feasible under all constraints.

        Parameters
        ----------
        design_vars:
            A dictionary of design variable assignments.

        Returns
        -------
        bool
            True if all constraints are satisfied, False otherwise.
        """
        if self.topology is None:
            return False
        metrics = self.topology.evaluate(design_vars)
        return all(constraint(metrics, self.topology) for constraint in self.constraints)


@dataclass
class Solution:
    """
    Encapsulates the result of solving an optimization problem.

    Stores the chosen topology name, the design variables that define the
    solution, the computed metrics, and the objective values.
    """

    topology_name: str
    design_variables: Dict[str, Any]
    metrics: Dict[str, Any]
    objectives: List[float]
