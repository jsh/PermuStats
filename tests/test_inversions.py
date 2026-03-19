from permustats.analysis import decompose_cycles, Analyzer
from permustats.math_utils import mahonian
from permustats.plugins import InversionPlugin


def test_inversion_math_identity_n4():
    """
    Verify that the empirical distribution of inversions for N=4
    exactly matches the Mahonian theoretical distribution.
    """
    import itertools

    n = 4

    # 1. Collect all permutations for N=4 (4! = 24)
    # Using the same logic as the engine's exhaustive mode
    results = [
        decompose_cycles(list(p)) for p in itertools.permutations(range(1, n + 1))
    ]

    # 2. Use the Analyzer to build the frequency distribution
    analyzer = Analyzer(results)
    dist = analyzer.frequency_distribution("inversions")

    # 3. Verify against Mahonian(4, k)
    # Expected sequence for N=4: 1, 3, 5, 6, 5, 3, 1
    max_inv = n * (n - 1) // 2
    for k in range(max_inv + 1):
        actual_count = dist.get(k, 0)
        expected_count = mahonian(n, k)
        assert actual_count == expected_count, (
            f"Mismatch at k={k}: expected {expected_count}, got {actual_count}"
        )


def test_inversion_plugin_extraction():
    """Ensure the plugin correctly extracts the field from the result object."""
    # Hand-crafted permutation with 3 inversions: [3, 2, 1] (for n=3)
    # (3,2), (3,1), (2,1)
    res = decompose_cycles([3, 2, 1])
    plugin = InversionPlugin()

    assert res.inversions == 3
    assert plugin.calculate(res) == 3
