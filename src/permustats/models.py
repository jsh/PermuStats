from typing import NamedTuple


class AnalysisResult(NamedTuple):
    permutation: list[int]
    cycles: list[list[int]]
    total_cycles: int
    fixed_points: int
    lengths_sequence: list[int]
    cycle_lengths: dict[int | float, int]
    inversions: int
    descents: int
    exceedances: int
    major_index: int
