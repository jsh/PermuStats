from generator import PermutationGenerator


def test_exhaustive_count_and_uniqueness():
    """Verify exhaustive(3) produces 3! (6) unique permutations."""
    gen = PermutationGenerator.exhaustive(3)
    results = list(gen)

    assert len(results) == 6
    # Ensure all are unique by converting to tuples (hashable) and checking set size
    assert len(set(tuple(p) for p in results)) == 6


def test_sample_quantity():
    """Verify sample(10, 100) yields exactly 100 permutations."""
    gen = PermutationGenerator.sample(10, 100)
    results = list(gen)

    assert len(results) == 100


def test_permutation_integrity():
    """Verify every permutation contains all integers from 0 to N-1 exactly once."""
    n = 5
    # Check a mix of both methods
    exhaustive_samples = list(PermutationGenerator.exhaustive(3))  # N=3
    random_samples = list(PermutationGenerator.sample(n, 10))  # N=5

    # Check random samples specifically
    for p in random_samples:
        assert sorted(p) == list(range(n))
        assert len(p) == n

    # Check exhaustive samples specifically
    for p in exhaustive_samples:
        assert sorted(p) == list(range(3))
