import statistics
from typing import Callable
from permustats.models import AnalysisResult
from permustats.validation import OEISLookup


def decompose_cycles(permutation: list[int], base: int = 1) -> AnalysisResult:
    """
    Decomposes a permutation into disjoint cycles.

    Args:
        permutation: The list of integers representing the permutation.
        base: The starting index of the permutation (usually 1 or 0).
              Defaults to 1 per project standards.
    """
    n = len(permutation)
    if n == 0:
        return AnalysisResult([], [], 0, 0, {}, [])

    visited = [False] * n
    cycles: list[list[int]] = []
    lengths_sequence: list[int] = []

    for i in range(n):
        if not visited[i]:
            curr_cycle = []
            curr_idx = i
            try:
                while not visited[curr_idx]:
                    visited[curr_idx] = True
                    val = permutation[curr_idx]
                    curr_cycle.append(val)

                    # Performance: Subtract base here instead of pre-allocating a map.
                    # Robustness: Explicit base ensures we don't guess indexing.
                    curr_idx = val - base

                cycles.append(curr_cycle)
                lengths_sequence.append(len(curr_cycle))
            except IndexError:
                # This ensures we catch values that don't point back into the valid range
                raise ValueError(
                    f"Permutation value {permutation[curr_idx]} is out of bounds "
                    f"for N={n} with base {base}."
                )

    # Frequency Map (unchanged logic, just ensuring clean types)
    freq_map: dict[int, int] = {}
    for length in lengths_sequence:
        freq_map[length] = freq_map.get(length, 0) + 1

    return AnalysisResult(
        permutation=permutation,
        cycles=cycles,
        total_cycles=len(cycles),
        fixed_points=sum(1 for c in cycles if len(c) == 1),
        cycle_lengths=freq_map,
        lengths_sequence=lengths_sequence,
    )


class Analyzer:
    """Aggregates multiple AnalysisResults to provide statistical insights."""

    def __init__(self, results: list[AnalysisResult]):
        self.results = results

    # def report(self, metric: str, n_size: int) -> None:
    #     """Enhanced Reporter: Handles Stats, OEIS, and Distributions."""
    #     from permustats.validation import OEISLookup

    #     if not self.results:
    #         print("No results to analyze.")
    #         return

    #     avg = self.mean(metric)
    #     dist = self.frequency_distribution(metric)

    #     print(f"Mean:         {avg:.4f}")

    #     # Logic from your commented-out code:
    #     # If the metric is a scalar count, we can look it up in OEIS
    #     if metric in ["total_cycles", "fixed_points"]:
    #         # We sort the dict to ensure the sequence order is [0, 1, 2... k]
    #         oeis_str = OEISLookup.format_sequence(n_size, dist)
    #         print(f"OEIS Sequence: {oeis_str}")
    #     else:
    #         # For complex metrics like cycle-lengths (partitions)
    #         print(f"Distribution: {dict(sorted(dist.items()))}")

    def report(self, metric: str, n_size: int) -> None:
        """Enhanced Reporter: Handles Stats, OEIS, and Distributions."""
        if not self.results:
            print("No results to analyze.")
            return

        # 1. Handle Scalar Metrics (Counts)
        if metric in ["total_cycles", "fixed_points"]:
            avg = self.mean(metric)
            dist = self.frequency_distribution(metric)

            oeis_str = OEISLookup.format_sequence(n_size, dist)

            print(f"Mean:         {avg:.4f}")
            print(f"OEIS Sequence: {oeis_str}")

        # 2. Handle Vector Metrics (Sequences/Lists)
        elif metric == "lengths_sequence":
            # For cycle-lengths, we aggregate all lengths into one big distribution
            all_lengths = []
            for r in self.results:
                all_lengths.extend(r.lengths_sequence)

            # Use your frequency_distribution logic but on the flattened list
            dist = {}
            for length in all_lengths:
                dist[length] = dist.get(length, 0) + 1

            # Note: We skip avg because statistics.mean(all_lengths)
            # would be the mean length of a cycle, which is a different stat.
            print(f"Distribution: {dict(sorted(dist.items()))}")

    def _get_values(
        self, getter: Callable[[AnalysisResult], int | float]
    ) -> list[int | float]:
        """Helper to extract specific metrics from the results set."""
        return [getter(r) for r in self.results]

    def mean(self, metric: str = "total_cycles") -> float:
        """Calculates the mean for a given attribute."""
        values = self._get_values(lambda r: getattr(r, metric))
        return statistics.mean(values) if values else 0.0

    def variance(self, metric: str = "total_cycles") -> float:
        """Calculates the population variance (pvariance) for a given attribute."""
        values = self._get_values(lambda r: getattr(r, metric))
        # Use pvariance for theoretical combinatorial consistency
        return statistics.pvariance(values) if values else 0.0

    def frequency_distribution(
        self, metric: str = "total_cycles"
    ) -> dict[int | float, int]:
        """Returns a frequency map of the specified metric."""
        values = self._get_values(lambda r: getattr(r, metric))
        dist: dict[int | float, int] = {}
        for v in values:
            dist[v] = dist.get(v, 0) + 1
        return dist
