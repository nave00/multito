"""Cost module providing cost terms and an assembler for total cost computation."""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any


@dataclass
class CostTerm:
    """Represents a single cost component with an associated weight and computation function."""
    name: str
    weight: float
    func: Callable[[Dict[str, Any]], float]

    def evaluate(self, context: Dict[str, Any]) -> float:
        """Evaluate the cost term on the given context, returning the weighted contribution."""
        return self.weight * self.func(context)


@dataclass
class CostAssembler:
    """Aggregates multiple CostTerms to compute a total cost."""
    terms: List[CostTerm] = field(default_factory=list)

    def add_term(self, term: CostTerm) -> None:
        """Add a new cost term to the assembler."""
        self.terms.append(term)

    def total_cost(self, context: Dict[str, Any]) -> float:
        """Compute the total cost as the sum of all weighted cost terms."""
        return sum(term.evaluate(context) for term in self.terms)


# Example cost functions for convenience
def loss_cost(context: Dict[str, Any]) -> float:
    """Return the loss component from the context."""
    return context.get("loss", 0.0)


def weight_cost(context: Dict[str, Any]) -> float:
    """Return the weight component from the context."""
    return context.get("weight", 0.0)


def area_cost(context: Dict[str, Any]) -> float:
    """Return the area component from the context."""
    return context.get("area", 0.0)


def dc_loss_cost(context: Dict[str, Any]) -> float:
    """Return the DC resistive loss component from the context."""
    return context.get("dc_loss", context.get("loss_dc", 0.0))


def ac_loss_cost(context: Dict[str, Any]) -> float:
    """Return the AC resistive loss component from the context."""
    return context.get("ac_loss", context.get("loss_ac", 0.0))


def temperature_cost(context: Dict[str, Any]) -> float:
    """Return the temperature rise component from the context."""
    return context.get("temperature", 0.0)


def emi_cost(context: Dict[str, Any]) -> float:
    """Return the electromagnetic interference component from the context."""
    return context.get("emi", 0.0)
