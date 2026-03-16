from typing import Any

from permustats.models import AnalysisResult
from permustats.validation import OEISLookup


def decompose_cycles(permutation: list[int], base: int = 1) -> AnalysisResult:
    """
    Decomposes a permutation into disjoint cycles using a boolean mask.
    """
    n = len(permutation)
    if n == 0:
        return AnalysisResult([], [], 0, 0, {}, [])

    # High-speed boolean mask
    visited = [False] * n
    cycles: list[list[int]] = []
    lengths_sequence: list[int] = []
    fixed_points = 0
    freq_map: dict[int, int] = {}

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

                # Single-pass metrics
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
    )


class Analyzer:
    """Universal Streaming Analyzer: One pass, all stats cached."""

    def __init__(self, results_iterator: Any):
        self._iterator = results_iterator
        self._consumed = False

        # We cache everything so we don't need to know the metric upfront
        self._stats: dict[str, dict[str, Any]] = {
            "total_cycles": {"mean": 0.0, "m2": 0.0, "dist": {}},
            "fixed_points": {"mean": 0.0, "m2": 0.0, "dist": {}},
            "lengths_sequence": {"dist": {}},
        }
        self._count = 0

    def _ensure_processed(self) -> None:
        if self._consumed:
            return

        for res in self._iterator:
            self._count += 1
            # Process all potential metrics in one discovery walk
            for m in ["total_cycles", "fixed_points"]:
                val = getattr(res, m)
                s = self._stats[m]
                # Welford's
                delta = val - s["mean"]
                s["mean"] += delta / self._count
                s["m2"] += delta * (val - s["mean"])
                # Distribution
                s["dist"][val] = s["dist"].get(val, 0) + 1

            # Handle the vector metric
            for length in res.lengths_sequence:
                self._stats["lengths_sequence"]["dist"][length] = (
                    self._stats["lengths_sequence"]["dist"].get(length, 0) + 1
                )

        self._consumed = True

    def mean(self, metric: str = "total_cycles") -> float:
        self._ensure_processed()
        m = metric.replace("-", "_")
        return self._stats.get(m, {}).get("mean", 0.0)

    def variance(self, metric: str = "total_cycles") -> float:
        self._ensure_processed()
        m = metric.replace("-", "_")
        s = self._stats.get(m, {})
        return s.get("m2", 0.0) / self._count if self._count > 0 else 0.0

    def frequency_distribution(
        self, metric: str = "total_cycles"
    ) -> dict[int | float, int]:
        self._ensure_processed()
        m = metric.replace("-", "_")
        # Cast to satisfy ty's type rigor
        return self._stats.get(m, {}).get("dist", {})  # type: ignore

    def report(self, metric: str, n_size: int) -> None:
        self._ensure_processed()
        m = metric.replace("-", "_")

        if m == "lengths_sequence":
            dist = self._stats[m]["dist"]
            print(f"Distribution: {dict(sorted(dist.items()))}")
        else:
            # Cast the dict to satisfy ty's invariant key requirement
            # dict[int, int] -> dict[int | float, int]
            dist: dict[int | float, int] = self._stats[m]["dist"]  # type: ignore

            oeis_str = OEISLookup.format_sequence(n_size, dist)
            print(f"Mean:          {self.mean(m):.4f}")
            print(f"OEIS Sequence: {oeis_str}")
