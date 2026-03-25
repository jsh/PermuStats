from __future__ import annotations

from typing import Iterable, TYPE_CHECKING, cast, Dict, Union, TypedDict

from permustats.validation import OEISLookup
from permustats.models import AnalysisResult


# Define the schema for ty
class MetricStats(TypedDict):
    mean: float
    m2: float
    dist: Dict[Union[int, float], int]
    count: int


try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None  # type: ignore

if TYPE_CHECKING:
    pass


def decompose_cycles(
    permutation: list[int], base: int = 1, target_metric: str | None = None
) -> AnalysisResult:
    n = len(permutation)
    if n == 0:
        return AnalysisResult([], [], 0, 0, [], {}, 0, 0, 0, 0)

    # 1. Inversion Counting (O(N log N)) - Only if needed
    inversions = 0
    if target_metric in (None, "inversions", "major_index"):
        bit = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            val_norm = permutation[i] - base + 1
            # Inline Query logic
            idx, s = val_norm - 1, 0
            while idx > 0:
                s += bit[idx]
                idx -= idx & (-idx)
            inversions += s
            # Inline Update logic
            idx = val_norm
            while idx <= n:
                bit[idx] += 1
                idx += idx & (-idx)

    # 2. Descent & Major Index (O(N))
    descents = major_index = exceedances = 0
    for i in range(n):
        val = permutation[i]
        if val > (i + base):
            exceedances += 1
        if i < n - 1 and val > permutation[i + 1]:
            descents += 1
            major_index += i + 1

    # 3. Cycle Decomposition (O(N)) - Only if needed
    all_cycles: list[list[int]] = []
    total_cycles = fixed_points = 0
    lengths_sequence: list[int] = []

    if target_metric in (
        None,
        "total_cycles",
        "fixed_points",
        "lengths_sequence",
        "cycle_counts",
    ):
        visited = [False] * n
        for i in range(n):
            if visited[i]:
                continue
            total_cycles += 1
            curr_idx, current_cycle = i, []
            while not visited[curr_idx]:
                visited[curr_idx] = True
                val = permutation[curr_idx]
                current_cycle.append(val)
                curr_idx = val - base
            all_cycles.append(current_cycle)
            c_len = len(current_cycle)
            lengths_sequence.append(c_len)
            if c_len == 1:
                fixed_points += 1

    # FIX: Rename 'l' to 'length' for Ruff E741
    cycle_lengths: dict[int | float, int] = {}
    if lengths_sequence:
        for length in set(lengths_sequence):
            cycle_lengths[length] = lengths_sequence.count(length)

    return AnalysisResult(
        permutation=permutation,
        cycles=all_cycles,
        total_cycles=total_cycles,
        fixed_points=fixed_points,
        lengths_sequence=sorted(lengths_sequence),
        cycle_lengths=cycle_lengths,
        inversions=inversions,
        descents=descents,
        exceedances=exceedances,
        major_index=major_index,
    )


class Analyzer:
    def __init__(self, results_iterator: Iterable[AnalysisResult]):
        self._iterator = results_iterator
        self._consumed = False
        self._count = 0
        self._scalar_metrics = [
            "total_cycles",
            "fixed_points",
            "inversions",
            "descents",
            "exceedances",
            "major_index",
        ]

        # Initialize with the explicit TypedDict schema
        self._stats: Dict[str, MetricStats] = {
            m: {
                "mean": 0.0,
                "m2": 0.0,
                "dist": cast(Dict[Union[int, float], int], {}),
                "count": 0,
            }
            for m in self._scalar_metrics
        }
        self._stats["lengths_sequence"] = {
            "mean": 0.0,
            "m2": 0.0,
            "dist": cast(Dict[Union[int, float], int], {}),
            "count": 0,
        }

    def _ensure_processed(self) -> None:
        if self._consumed:
            return

        # Pulling these into local variables minimizes dictionary lookups
        stats = self._stats
        metrics = self._scalar_metrics
        v_stats = stats["lengths_sequence"]

        for res in self._iterator:
            self._count += 1

            # Scalar Metrics Pass
            for m_name in metrics:
                val = getattr(res, m_name)
                s = stats[m_name]

                # Now ty knows s['count'] is an int
                s["count"] += 1

                delta = val - s["mean"]
                s["mean"] += delta / s["count"]
                s["m2"] += delta * (val - s["mean"])

                # dist is now guaranteed to be a Dict
                s["dist"][val] = s["dist"].get(val, 0) + 1

            # Vector Metric Pass (lengths_sequence)
            for length in res.lengths_sequence:
                v_stats["count"] += 1
                v_stats["dist"][length] = v_stats["dist"].get(length, 0) + 1

        self._consumed = True

    def mean(self, metric: str = "total_cycles") -> float:
        self._ensure_processed()
        m = metric.replace("-", "_")
        # Explicit access to the TypedDict field
        return self._stats.get(m, {"mean": 0.0})["mean"]

    def variance(self, metric: str = "total_cycles") -> float:
        self._ensure_processed()
        m = metric.replace("-", "_")
        stats = self._stats.get(m)

        if not stats or stats["count"] == 0:
            return 0.0

        return stats["m2"] / stats["count"]

    def frequency_distribution(
        self, metric: str = "total_cycles"
    ) -> Dict[Union[int, float], int]:
        self._ensure_processed()
        m = metric.replace("-", "_")
        stats = self._stats.get(m)
        return stats["dist"] if stats else {}

    def report(self, metric: str, n_size: int) -> None:
        """Generates a summary report including OEIS sequence matching."""
        self._ensure_processed()
        m = metric.replace("-", "_")
        if m == "cycle_counts":
            m = "total_cycles"

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

    def plot(self, metric: str, save_path: str | None = None) -> None:
        """
        Generates a bar chart for the discrete frequency distribution.
        """
        if plt is None:
            raise RuntimeError(
                "Plotting requires matplotlib. Install it with: pip install 'permustats[plot]'"
            )

        dist = self.frequency_distribution(metric)
        if not dist:
            print(f"Warning: No data to plot for metric '{metric}'")
            return

        x_values = sorted(dist.keys())
        y_values = [dist[k] for k in x_values]

        plt.figure(figsize=(10, 6))
        plt.bar(x_values, y_values, color="skyblue", edgecolor="navy", align="center")

        plt.title(
            f"Distribution of {metric.replace('_', ' ').title()} (N={self._count})"
        )
        plt.xlabel(metric.replace("_", " ").title())
        plt.ylabel("Frequency")
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Ensure x-axis only shows integers
        plt.xticks(x_values)

        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        else:
            plt.show()

    def add_result(self, res: AnalysisResult) -> None:
        """The 'Push' entry point: processes a single result immediately."""
        self._count += 1
        stats = self._stats
        metrics = self._scalar_metrics

        for m_name in metrics:
            val = getattr(res, m_name)
            s = stats[m_name]
            s["count"] += 1
            delta = val - s["mean"]
            s["mean"] += delta / s["count"]
            s["m2"] += delta * (val - s["mean"])
            s["dist"][val] = s["dist"].get(val, 0) + 1

        v_stats = stats["lengths_sequence"]
        for length in res.lengths_sequence:
            v_stats["count"] += 1
            v_stats["dist"][length] = v_stats["dist"].get(length, 0) + 1
