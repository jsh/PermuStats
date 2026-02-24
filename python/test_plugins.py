import pytest
from transformers import CycleFormTransformer

@pytest.fixture
def transformer():
    return CycleFormTransformer()

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
