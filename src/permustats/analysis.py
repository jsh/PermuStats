from dataclasses import dataclass
import statistics


@dataclass(frozen=True)
class AnalysisResult:
    """The structural breakdown of a single permutation."""

    permutation: list[int]
    cycles: list[list[int]]
    total_cycles: int
    fixed_points: int
    cycle_lengths: dict[int, int]


def decompose_cycles(permutation: list[int]) -> AnalysisResult:
    """
    Decomposes a permutation into disjoint cycles in O(N) time.
    Supports both 0-indexed and 1-indexed input arrays.
    """
    n = len(permutation)
    visited = [False] * n
    cycles = []

    # Normalize to 0-indexing for internal pointer logic
    offset = min(permutation)
    adj_p = [x - offset for x in permutation]

    for i in range(n):
        if not visited[i]:
            curr_cycle = []
            curr_idx = i
            while not visited[curr_idx]:
                visited[curr_idx] = True
                curr_cycle.append(curr_idx + offset)
                curr_idx = adj_p[curr_idx]
            cycles.append(curr_cycle)

    lengths = [len(c) for c in cycles]
    length_counts = {}
    for length in lengths:
        length_counts[length] = length_counts.get(length, 0) + 1

    return AnalysisResult(
        permutation=permutation,
        cycles=cycles,
        total_cycles=len(cycles),
        fixed_points=length_counts.get(1, 0),
        cycle_lengths=length_counts,
    )


class Analyzer:
    """Aggregates multiple AnalysisResults to provide statistical insights."""

    def __init__(self, results: list[AnalysisResult]):
        self.results = results
        # Extract the total cycle counts for aggregate math
        self.counts = [r.total_cycles for r in results]

    def mean(self) -> float:
        return statistics.mean(self.counts) if self.counts else 0.0

    def variance(self) -> float:
        return statistics.variance(self.counts) if len(self.counts) > 1 else 0.0

    def frequency_distribution(self) -> dict[int, int]:
        dist = {}
        for c in self.counts:
            dist[c] = dist.get(c, 0) + 1
        return dist
