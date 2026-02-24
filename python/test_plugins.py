import pytest
from transformers import CycleFormTransformer, FixedPointCounter, CycleLengthCounter

@pytest.fixture
def transformer():
    return CycleFormTransformer()

@pytest.fixture
def fp_counter():
    return FixedPointCounter()

@pytest.fixture
def cl_counter():
    return CycleLengthCounter()

def test_fixed_points(transformer):
    """Verify identity permutation [0, 1, 2] maps to individual cycles."""
    # Each element points to itself
    assert transformer.process([0, 1, 2]) == [[0], [1], [2]]

def test_simple_swap(transformer):
    """Verify [1, 0, 2] maps to one swap and one fixed point."""
    # 0->1, 1->0 (cycle); 2->2 (fixed point)
    result = transformer.process([1, 0, 2])
    assert [0, 1] in result
    assert [2] in result
    assert len(result) == 2

def test_long_cycle(transformer):
    """Verify [1, 2, 0] maps to a single full-length cycle."""
    # 0->1, 1->2, 2->0
    assert transformer.process([1, 2, 0]) == [[0, 1, 2]]

def test_fixed_point_counter(fp_counter):
    """Verify FixedPointCounter identifies identity vs derangements."""
    assert fp_counter.process([0, 1, 2]) == 3  # All are fixed
    assert fp_counter.process([1, 2, 0]) == 0  # None are fixed (derangement)
    assert fp_counter.process([0, 2, 1]) == 1  # Only 0 is fixed

def test_cycle_length_counter(transformer, cl_counter):
    """Verify CycleLengthCounter extracts lengths correctly."""
    # Test with a single long cycle [1, 2, 0] -> [[0, 1, 2]]
    cycles = transformer.process([1, 2, 0])
    lengths = cl_counter.process(cycles)
    assert lengths == [3]

    # Test with mixed cycles [1, 0, 2] -> [[0, 1], [2]]
    cycles_mixed = transformer.process([1, 0, 2])
    lengths_mixed = cl_counter.process(cycles_mixed)
    assert sorted(lengths_mixed) == [1, 2]
