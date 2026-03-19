import pytest
from permustats.math_utils import harmonic_number, subfactorial, stirling_first
from permustats.math_utils import mahonian
from permustats.engine import PermuStatsEngine
from permustats.plugins.inversions import InversionInspector
from permustats.analysis import Analyzer


def test_harmonic_numbers():
    assert harmonic_number(0) == 0.0
    assert harmonic_number(1) == 1.0
    assert harmonic_number(2) == 1.5
    assert harmonic_number(4) == pytest.approx(2.0833333333)


def test_subfactorials():
    # !n: 1, 0, 1, 2, 9, 44...
    assert subfactorial(0) == 1
    assert subfactorial(1) == 0
    assert subfactorial(2) == 1
    assert subfactorial(3) == 2
    assert subfactorial(4) == 9
    assert subfactorial(6) == 265


def test_stirling_numbers():
    # [3, 2] = 3
    # [4, 2] = 11
    assert stirling_first(3, 2) == 3
    assert stirling_first(4, 2) == 11
    assert stirling_first(5, 3) == 35
    assert stirling_first(6, 1) == 120  # (6-1)!


def test_mahonian_sequence_n5():
    """Verify mahonian(n, k) produces the expected sequence for N=5."""
    # OEIS A008302: 1, 4, 9, 15, 20, 22, 20, 15, 9, 4, 1
    n = 5
    max_inv = n * (n - 1) // 2  # 10
    actual = [mahonian(n, k) for k in range(max_inv + 1)]
    expected = [1, 4, 9, 15, 20, 22, 20, 15, 9, 4, 1]

    assert actual == expected
    assert actual == list(reversed(actual)), "Mahonian row must be a palindrome"


def test_mahonian_vs_engine_exhaustive_n5():
    """Verify the Engine's inversion counting matches Mahonian theory for N=5."""
    n = 5
    inspector = InversionInspector()
    engine = PermuStatsEngine(plugin=inspector)

    # Run exhaustive study (120 permutations)
    results = list(engine.run_study(n=n, num_samples=None))

    # Build the empirical distribution
    dist: dict[int, int] = {}
    for r in results:
        dist[r.inversions] = dist.get(r.inversions, 0) + 1

    # Compare each point in the distribution to the math_utils ground truth
    max_inv = n * (n - 1) // 2
    for k in range(max_inv + 1):
        assert dist.get(k, 0) == mahonian(n, k), f"Mismatch at k={k}"


def test_stochastic_inversion_mean_n100():
    """Verify stochastic mean for N=100 is n(n-1)/4 = 2475.0."""
    n = 100
    samples = 5000
    inspector = InversionInspector()
    engine = PermuStatsEngine(plugin=inspector)

    # Use the streaming Analyzer to avoid memory bloat
    results = engine.run_study(n=n, num_samples=samples)
    analyzer = Analyzer(results)

    expected_mean = (n * (n - 1)) / 4
    # With 5k samples, we expect to be within 1-2% of the theoretical mean
    # Pass the metric name explicitly
    assert analyzer.mean("inversions") == pytest.approx(expected_mean, rel=0.02)
