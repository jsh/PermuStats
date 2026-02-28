from typing import Iterable, List, Any, Optional
from plugins import PermuPlugin
from transformers import CycleTransformer


class PermuStatsEngine:
    """The core orchestrator for permutation analysis."""

    def __init__(
        self, plugin: PermuPlugin, transformer: Optional[CycleTransformer] = None
    ):
        self.plugin = plugin
        self.transformer = transformer

    def process(self, data: Iterable[List[int]]) -> Iterable[Any]:
        """Memory-efficient generator for processing permutations."""
        for p in data:
            # Transform if needed (e.g., to cycles), otherwise use raw permutation
            processed_data = self.transformer.transform(p) if self.transformer else p
            yield self.plugin.calculate(processed_data)

    def calculate_p_value(self, observed: float, permutations: List[float]) -> float:
        """
        Calculates p-value: (count of perms >= observed) / total perms.
        Uses float-safe comparison logic.
        """
        if not permutations:
            return 0.0

        count = sum(1 for p in permutations if p >= observed)
        return count / len(permutations)
