from dataclasses import dataclass


@dataclass(slots=True, frozen=True)  # Using slots for memory efficiency
class AnalysisResult:
    permutation: list[int]
    cycles: list[list[int]]
    total_cycles: int
    fixed_points: int
    cycle_lengths: dict[int, int]
    lengths_sequence: list[int]
