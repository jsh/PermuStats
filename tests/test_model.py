from __future__ import annotations
import pytest
from permustats.models import AnalysisResult


def test_analysis_result_immutability():
    """Verify that AnalysisResult is frozen and uses slots."""
    res = AnalysisResult(
        permutation=[1, 2],
        cycles=[[1], [2]],
        total_cycles=2,
        fixed_points=2,
        cycle_lengths={1: 2},
        lengths_sequence=[1, 1],
        inversions=0,
        descents=0,
        major_index=0,
        exceedances=0,
    )

    # Change FrozenInstanceError to AttributeError
    with pytest.raises(AttributeError):
        res.total_cycles = 3  # type: ignore[invalid-assignment]

    # Check slots (should not have a __dict__)
    assert not hasattr(res, "__dict__")


def test_analysis_result_fields():
    """Ensure all fields are correctly stored and accessible."""
    res = AnalysisResult(
        permutation=[2, 1],
        cycles=[[2, 1]],
        total_cycles=1,
        fixed_points=0,
        cycle_lengths={2: 1},
        lengths_sequence=[2],
        inversions=1,
        descents=1,
        major_index=1,
        exceedances=1,
    )
    assert res.permutation == [2, 1]
    assert res.total_cycles == 1
