from __future__ import annotations
import pytest
from dataclasses import FrozenInstanceError
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
    )

    # Check immutability
    with pytest.raises(FrozenInstanceError):
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
    )
    assert res.permutation == [2, 1]
    assert res.total_cycles == 1
