import random
from typing import Iterable, Any, Optional

from permustats.generator import PermutationGenerator
from permustats.analysis import AnalysisResult, decompose_cycles


class PermuStatsEngine:
    """The core orchestrator for permutation analysis."""

    def __init__(
        self,
        plugin: Any,
        transformer: Optional[Any] = None,
        seed: Optional[int] = None,
        base: int = 1,
    ):
        self.plugin = plugin
        self.transformer = transformer
        self.base = base
        # Create a local random instance to avoid global state pollution
        self.rng = random.Random(seed)

    def run_study(
        self, n: int, num_samples: int | None = None
    ) -> Iterable[AnalysisResult]:
        """
        Decides between Exhaustive and Sample based on user intent.
        """
        # If the user didn't ask for a specific sample count, go Exhaustive.
        if num_samples is None:
            self.mode = "Exhaustive"
            stream = PermutationGenerator.exhaustive(n)
        else:
            self.mode = "Sample"
            stream = PermutationGenerator.sample(n, num_samples, self.rng)

        return self.process(stream)

    def process(self, data: Iterable[list[int]]) -> Iterable[AnalysisResult]:
        """
        Transforms raw permutations into rich AnalysisResult objects.
        Optimized for high-throughput streaming.
        """
        # We check the plugin once outside the loop to keep the inner loop hot.
        if self.plugin:
            for p in data:
                result = decompose_cycles(p, base=self.base)
                # Correcting the method name from 'execute' back to 'calculate'
                self.plugin.calculate(result)
                yield result
        else:
            # The "Fast Path" for standard runs
            for p in data:
                yield decompose_cycles(p, base=self.base)

    def calculate_p_value(self, observed: float, permutations: list[float]) -> float:
        """
        Calculates p-value: (count of perms >= observed) / total perms.
        Uses float-safe comparison logic.
        """
        if not permutations:
            return 0.0

        count = sum(1 for p in permutations if p >= observed)
        return count / len(permutations)
