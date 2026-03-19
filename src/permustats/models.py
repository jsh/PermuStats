from dataclasses import dataclass


@dataclass(slots=True, frozen=True)  # Using slots for memory efficiency
class AnalysisResult:
    permutation: list[int]
    cycles: list[list[int]]
    total_cycles: int
    fixed_points: int
    lengths_sequence: list[int]
    cycle_lengths: dict[int | float, int]
    inversions: int
    descents: int
    major_index: int
