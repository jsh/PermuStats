from __future__ import annotations
from typing import Any, Iterable

from permustats.validation import OEISLookup
from permustats.models import AnalysisResult


def decompose_cycles(permutation: list[int], base: int = 1) -> AnalysisResult:
    """
    Decomposes a permutation into disjoint cycles using a boolean mask.
    """
    n = len(permutation)
    if n == 0:
        return AnalysisResult([], [], 0, 0, {}, [], 0)

    # 1. Inversion Counting (O(N^2))
    # We do this first while 'permutation' is fresh in the cache
    inv_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if permutation[i] > permutation[j]:
                inv_count += 1

    # 2. Cycle Decomposition
    visited = [False] * n
    cycles: list[list[int]] = []
    lengths_sequence: list[int] = []
    fixed_points = 0
    freq_map: dict[int | float, int] = {}

    for i in range(n):
        if not visited[i]:
            curr_cycle = []
            curr_idx = i
            try:
                while not visited[curr_idx]:
                    visited[curr_idx] = True
                    val = permutation[curr_idx]
                    curr_cycle.append(val)
                    curr_idx = val - base

                c_len = len(curr_cycle)
                cycles.append(curr_cycle)
                lengths_sequence.append(c_len)

                if c_len == 1:
                    fixed_points += 1
                freq_map[c_len] = freq_map.get(c_len, 0) + 1
            except IndexError:
                raise ValueError(
                    f"Permutation value {permutation[curr_idx]} is out of bounds "
                    f"for N={n} with base {base}."
                )

    return AnalysisResult(
        permutation=permutation,
        cycles=cycles,
        total_cycles=len(cycles),
        fixed_points=fixed_points,
        cycle_lengths=freq_map,
        lengths_sequence=lengths_sequence,
        inversions=inv_count,
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
        """The 'JIT' Engine: Exhausts the generator and populates all stats."""
        if self._consumed:
            return

        for res in self._iterator:
            self._count += 1

            # 1. Scalar Metrics (Welford's)
            # Added "inversions" to the tracking list
            for m in ["total_cycles", "fixed_points", "inversions"]:
                val = getattr(res, m)
                s = self._stats[m]

                # Update running mean and M2 (Welford's)
                delta = val - s["mean"]
                s["mean"] += delta / self._count
                delta2 = val - s["mean"]
                s["m2"] += delta * delta2

                # Update frequency distribution
                s["dist"][val] = s["dist"].get(val, 0) + 1

            # 2. Vector Metrics (Lengths Sequence)
            # We track the global frequency of every cycle length encountered
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
