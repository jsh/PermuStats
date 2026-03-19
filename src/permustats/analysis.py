from __future__ import annotations
from typing import Any, Iterable
import dataclasses

from permustats.validation import OEISLookup
from permustats.models import AnalysisResult


def decompose_cycles(permutation: list[int], base: int = 1) -> AnalysisResult:
    """
    Transforms a permutation into a rich AnalysisResult.
    Handles 0-based or 1-based indexing via the base parameter.
    """
    n = len(permutation)
    if n == 0:
        return AnalysisResult([], [], 0, 0, [], {}, 0, 0, 0)

    # 1. Inversion Counting (O(N^2))
    inversions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if permutation[i] > permutation[j]:
                inversions += 1

    # 2. Descent & Major Index Counting (O(N))
    descents = 0
    major_index = 0
    for i in range(n - 1):
        if permutation[i] > permutation[i + 1]:
            descents += 1
            major_index += i + 1  # Sum of 1-based positions

    # 3. Cycle Decomposition (O(N))
    visited = [False] * n
    total_cycles = 0
    fixed_points = 0
    lengths_sequence: list[int] = []
    all_cycles: list[list[int]] = []

    for i in range(n):
        if visited[i]:
            continue

        total_cycles += 1
        curr_idx = i
        current_cycle = []

        while not visited[curr_idx]:
            visited[curr_idx] = True
            val = permutation[curr_idx]
            current_cycle.append(val)

            try:
                curr_idx = val - base
                if not (0 <= curr_idx < n):
                    raise IndexError
            except IndexError:
                # Use 'val' from the loop scope for the error message
                raise ValueError(
                    f"Permutation value {val} is out of bounds for N={n} with base {base}."
                ) from None

        all_cycles.append(current_cycle)
        c_len = len(current_cycle)
        lengths_sequence.append(c_len)
        if c_len == 1:
            fixed_points += 1

    # 4. Frequency map for cycles
    cycle_lengths: dict[int | float, int] = {}
    for length in lengths_sequence:
        cycle_lengths[length] = cycle_lengths.get(length, 0) + 1

    return AnalysisResult(
        permutation=permutation,
        cycles=all_cycles,
        total_cycles=total_cycles,
        fixed_points=fixed_points,
        lengths_sequence=sorted(lengths_sequence),
        cycle_lengths=cycle_lengths,
        inversions=inversions,
        descents=descents,
        major_index=major_index,
    )


class Analyzer:
    """
    Universal Streaming Analyzer.
    Uses Welford's Algorithm to compute running mean and variance in O(1) space.
    """

    def __init__(self, results_iterator: Iterable[AnalysisResult]):
        self._iterator = results_iterator
        self._consumed = False
        self._count = 0

        # Internal state for metrics
        # m2 is the sum of squares of differences from the mean
        self._stats: dict[str, dict[str, Any]] = {
            "total_cycles": {"mean": 0.0, "m2": 0.0, "dist": {}},
            "fixed_points": {"mean": 0.0, "m2": 0.0, "dist": {}},
            "inversions": {"mean": 0.0, "m2": 0.0, "dist": {}},
            "lengths_sequence": {"dist": {}},
        }

    def _ensure_processed(self) -> None:
        """The 'JIT' Engine: Dynamically discovers and processes all scalar metrics."""
        if self._consumed:
            return

        for res in self._iterator:
            self._count += 1

            # Dynamically discover all numerical fields in the AnalysisResult
            for field in dataclasses.fields(res):
                # We only want to run Welford's/Distributions on int or float metrics
                if field.type in (int, float):
                    m_name = field.name
                    val = getattr(res, m_name)

                    # Ensure the metric exists in our internal _stats cache
                    if m_name not in self._stats:
                        self._stats[m_name] = {"mean": 0.0, "m2": 0.0, "dist": {}}

                    s = self._stats[m_name]

                    # Welford's Algorithm (Stable Version)
                    delta = val - s["mean"]
                    s["mean"] += delta / self._count
                    delta2 = val - s["mean"]
                    s["m2"] += delta * delta2

                    # Frequency Distribution
                    s["dist"][val] = s["dist"].get(val, 0) + 1

            # Handle the special case for the vector metric (Cycle Lengths)
            # (This remains manual as it's a list[int], not a scalar)
            ls_dist = self._stats["lengths_sequence"]["dist"]
            for length in res.lengths_sequence:
                ls_dist[length] = ls_dist.get(length, 0) + 1

        self._consumed = True

    def mean(self, metric: str = "total_cycles") -> float:
        self._ensure_processed()
        m = metric.replace("-", "_")
        return self._stats.get(m, {}).get("mean", 0.0)

    def variance(self, metric: str = "total_cycles") -> float:
        """Returns the population variance (sigma squared)."""
        self._ensure_processed()
        if self._count == 0:
            return 0.0
        m = metric.replace("-", "_")
        return self._stats.get(m, {}).get("m2", 0.0) / self._count

    def frequency_distribution(
        self, metric: str = "total_cycles"
    ) -> dict[int | float, int]:
        self._ensure_processed()
        m = metric.replace("-", "_")
        # Cast to satisfy ty's type rigor for public API
        return self._stats.get(m, {}).get("dist", {})

    def report(self, metric: str, n_size: int) -> None:
        """Generates a summary report including OEIS sequence matching."""
        self._ensure_processed()
        m = metric.replace("-", "_")

        print(f"\n--- Statistics Report [{metric}] ---")
        print(f"Sample Size:    {self._count}")

        if m == "lengths_sequence":
            dist = self._stats[m]["dist"]
            print(f"Distribution:   {dict(sorted(dist.items()))}")
        else:
            dist = self._stats[m]["dist"]
            # Cast for OEIS matching
            oeis_dist: dict[int | float, int] = dist
            oeis_str = OEISLookup.format_sequence(n_size, oeis_dist)

            print(f"Mean:           {self.mean(m):.4f}")
            print(f"Variance:       {self.variance(m):.4f}")
            print(f"OEIS Sequence:  {oeis_str}")
