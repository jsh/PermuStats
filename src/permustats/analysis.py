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
    n = len(permutation)
    if n == 0:
        return AnalysisResult([], [], 0, 0, {})

    # Detect indexing: if 0 is present, it's 0-indexed.
    # Otherwise, assume 1-indexed.
    offset = 0 if 0 in permutation else 1

    visited = [False] * n
    cycles = []

    # Create the pointer map
    adj_p = [x - offset for x in permutation]

    for i in range(n):
        if not visited[i]:
            curr_cycle = []
            curr_idx = i
            try:
                while not visited[curr_idx]:
                    visited[curr_idx] = True
                    # Store the value as it was given (1-indexed or 0-indexed)
                    curr_cycle.append(permutation[curr_idx])
                    curr_idx = adj_p[curr_idx]
                cycles.append(curr_cycle)
            except IndexError:
                # This catches cases where a value in the perm is out of bounds
                # e.g., N=3 but permutation contains '5'
                raise ValueError(
                    f"Value in permutation out of bounds for N={n}: {permutation}"
                )

    # Calculate metrics
    total_cycles = len(cycles)
    fixed_points = sum(1 for c in cycles if len(c) == 1)
    lengths = {}
    for c in cycles:
        lengths[len(c)] = lengths.get(len(c), 0) + 1

    return AnalysisResult(
        permutation=permutation,
        cycles=cycles,
        total_cycles=total_cycles,
        fixed_points=fixed_points,
        cycle_lengths=lengths,
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
