from permustats.transformers import CycleTransformer


def test_cycle_transformer_basic():
    transformer = CycleTransformer()
    permutation = [2, 1, 3]
    # Decomposition: (1 2)(3)
    expected_cycles = [[1, 2], [3]]
    result = transformer.transform(permutation)

    actual_cycles = result.cycles if hasattr(result, "cycles") else result

    # Sort for canonical comparison: sort inner lists, then the outer list
    actual_sorted = sorted([sorted(c) for c in actual_cycles])
    expected_sorted = sorted([sorted(c) for c in expected_cycles])

    assert actual_sorted == expected_sorted


def test_cycle_transformer_longer():
    transformer = CycleTransformer()
    permutation = [2, 3, 1, 5, 4]
    # Decomposition: (1 2 3)(4 5)
    expected_cycles = [[1, 2, 3], [4, 5]]
    result = transformer.transform(permutation)

    actual_cycles = result.cycles if hasattr(result, "cycles") else result

    actual_sorted = sorted([sorted(c) for c in actual_cycles])
    expected_sorted = sorted([sorted(c) for c in expected_cycles])

    assert actual_sorted == expected_sorted


def test_cycle_transformer_identity():
    transformer = CycleTransformer()
    # 1. Update to 1-indexing
    permutation = [1, 2, 3, 4]

    # 2. Expected output should also be 1-indexed
    expected_cycles = [[1], [2], [3], [4]]

    # 3. Handle the Rich Object return type
    result = transformer.transform(permutation)

    # Check if transform() returns the object or just the cycles list
    # Based on our Engine refactor, it should likely be the object's cycles
    actual_cycles = result.cycles if hasattr(result, "cycles") else result

    actual_sorted = sorted([sorted(c) for c in actual_cycles])
    expected_sorted = sorted([sorted(c) for c in expected_cycles])

    assert actual_sorted == expected_sorted
