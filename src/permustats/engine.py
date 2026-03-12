import math
import random
from typing import Iterable, Any, Optional

from permustats.generator import PermutationGenerator
from permustats.analysis import AnalysisResult, decompose_cycles


class PermuStatsEngine:
    """The core orchestrator for permutation analysis."""

    def __init__(
        self, plugin: Any, transformer: Optional[Any] = None, seed: Optional[int] = None
    ):
        self.plugin = plugin
        self.transformer = transformer
        # Create a local random instance to avoid global state pollution
        self.rng = random.Random(seed)

    def run_study(self, n: int, num_samples: int = 1000) -> Iterable[Any]:
        """The main entry point: Decides between exact and random permutations."""
        if math.factorial(n) <= 1000:
            self.mode = "Exhaustive"  # Add this to track mode for the printout
            stream = PermutationGenerator.exhaustive(n)
        else:
            self.mode = "Sample"
            stream = PermutationGenerator.sample(n, num_samples, self.rng)

        return self.process(stream)

    def process(self, data: Iterable[list[int]]) -> Iterable[AnalysisResult]:
        """
        Transforms raw permutations into rich AnalysisResult objects.
        Ensures the downstream Analyzer has structured data to work with.
        """
        for p in data:
            # 1. Decompose the raw permutation into a rich object
            result = decompose_cycles(p)

            # 2. If a plugin exists, let it do its specific calculation
            # (optional: you could store the plugin result inside the object)
            if self.plugin:
                # For now, we ensure we return the object so the Analyzer is happy
                # You might update AnalysisResult later to hold plugin-specific data
                pass

            yield result

    def calculate_p_value(self, observed: float, permutations: list[float]) -> float:
        """
        Calculates p-value: (count of perms >= observed) / total perms.
        Uses float-safe comparison logic.
        """
        if not permutations:
            return 0.0

        count = sum(1 for p in permutations if p >= observed)
        return count / len(permutations)
