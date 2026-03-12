import random
from permustats.generator import PermutationGenerator


def test_exhaustive_count_and_uniqueness():
    """Verify exhaustive(3) produces 3! (6) unique permutations."""
    gen = PermutationGenerator.exhaustive(3)
    results = list(gen)

    assert len(results) == 6
    # Ensure all are unique by converting to tuples (hashable) and checking set size
    assert len(set(tuple(p) for p in results)) == 6


def test_sample_quantity():
    """Verify sample(10, 100) yields exactly 100 permutations."""
    rng = random.Random(42)
    gen = PermutationGenerator.sample(10, 100, rng=rng)
    results = list(gen)

    assert len(results) == 100


def test_mixed_methods():
    rng = random.Random(42)
    n = 3  # 3! = 6

    # 1. Test Exhaustive: Should return exactly n! permutations
    exhaustive_samples = list(PermutationGenerator.exhaustive(n))
    assert len(exhaustive_samples) == 6
    assert [1, 2, 3] in exhaustive_samples
    assert len(set(tuple(p) for p in exhaustive_samples)) == 6  # All unique

    # 2. Test Sampled: Should return exactly the requested number of samples
    num_samples = 10
    random_samples = list(PermutationGenerator.sample(n, num_samples, rng=rng))
    assert len(random_samples) == num_samples
    # Each permutation in the sample should still be of length n
    assert all(len(p) == n for p in random_samples)


def test_permutation_integrity():
    """Verify every permutation contains all integers from 0 to N-1 exactly once."""
    rng = random.Random(42)
    n = 5
    # Check a mix of both methods
    exhaustive_samples = list(PermutationGenerator.exhaustive(3))  # N=3
    random_samples = list(PermutationGenerator.sample(n, 10, rng=rng))  # N=5

    # Check random samples specifically
    for p in random_samples:
        assert sorted(p) == [1, 2, 3, 4, 5]
        assert len(p) == n

    # Check exhaustive samples specifically
    for p in exhaustive_samples:
        assert sorted(p) == list(range(1, 4))
