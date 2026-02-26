import pytest
from transformers import CycleTransformer

def test_cycle_transformer_basic():
    transformer = CycleTransformer()
    permutation = [1, 0, 2]
    # Standard decomposition: (0 1)(2)
    expected_cycles = [[0, 1], [2]]
    actual_cycles = transformer.transform(permutation)
    
    # Sort for canonical comparison: sort inner lists, then the outer list
    actual_sorted = sorted([sorted(c) for c in actual_cycles])
    expected_sorted = sorted([sorted(c) for c in expected_cycles])
    
    assert actual_sorted == expected_sorted

def test_cycle_transformer_longer():
    transformer = CycleTransformer()
    permutation = [1, 2, 0, 4, 3]
    # Decomposition: (0 1 2)(3 4)
    expected_cycles = [[0, 1, 2], [3, 4]]
    actual_cycles = transformer.transform(permutation)
    
    actual_sorted = sorted([sorted(c) for c in actual_cycles])
    expected_sorted = sorted([sorted(c) for c in expected_cycles])
    
    assert actual_sorted == expected_sorted

def test_cycle_transformer_identity():
    transformer = CycleTransformer()
    permutation = [0, 1, 2, 3]
    # Identity: (0)(1)(2)(3)
    expected_cycles = [[0], [1], [2], [3]]
    actual_cycles = transformer.transform(permutation)
    
    actual_sorted = sorted([sorted(c) for c in actual_cycles])
    expected_sorted = sorted([sorted(c) for c in expected_cycles])
    
    assert actual_sorted == expected_sorted
