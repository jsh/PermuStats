import pytest
from permustats.engine import PermuStatsEngine
from permustats.analysis import Analyzer
from permustats.analysis import decompose_cycles


@pytest.mark.parametrize("n", [3, 4])
def test_mahonian_equidistribution(n):
    """
    Verify that Inversions and Major Index are equidistributed (Mahonian).
    The frequency maps for both statistics must be identical for exhaustive sets.
    """
    engine = PermuStatsEngine(plugin=None, base=1)

    # Run exhaustive study for N
    results = list(engine.run_study(n=n))
    analyzer = Analyzer(results)

    inv_dist = analyzer.frequency_distribution("inversions")
    maj_dist = analyzer.frequency_distribution("major_index")

    # Assertions for symmetry and identity
    assert inv_dist == maj_dist, f"Distributions differ for N={n}!"

    # Specific check for N=3: {0: 1, 1: 2, 2: 2, 3: 1}
    if n == 3:
        expected = {0: 1, 1: 2, 2: 2, 3: 1}
        assert inv_dist == expected


def test_mahonian_divergence_point():
    """Verify that statistics differ on a specific permutation but belong to the same set."""
    # Pi = [3, 1, 2] (base 1)
    res = decompose_cycles([3, 1, 2], base=1)
    # Inversions: (3,1), (3,2) -> 2
    # Major Index: Descent at pos 1 (3>1) -> 1
    assert res.inversions == 2
    assert res.major_index == 1
    assert res.inversions != res.major_index  # The "Divergence" proof


def test_mahonian_moments_n4():
    """Verify Mean and Variance for N=4 match Mahonian theory."""
    n = 4
    engine = PermuStatsEngine(plugin=None, base=1)
    results = list(engine.run_study(n=n))
    analyzer = Analyzer(results)

    # Theoretical Moments
    expected_mean = n * (n - 1) / 4  # 3.0
    expected_var = n * (n - 1) * (2 * n + 5) / 72  # 2.1666...

    for metric in ["inversions", "major_index"]:
        dist = analyzer.frequency_distribution(metric)

        # Calculate mean from frequency map
        total_count = sum(dist.values())
        mean = sum(k * v for k, v in dist.items()) / total_count

        # Calculate variance: E[X^2] - (E[X])^2
        mean_sq = sum((k**2) * v for k, v in dist.items()) / total_count
        variance = mean_sq - (mean**2)

        assert mean == pytest.approx(expected_mean)
        assert variance == pytest.approx(expected_var), f"{metric} variance mismatch!"


def test_major_index_specific_case():
    """Manual check for a known permutation: [3, 2, 1]."""

    # [3, 2, 1] base 1
    # Descent at pos 1: 3 > 2
    # Descent at pos 2: 2 > 1
    # Maj = 1 + 2 = 3
    res = decompose_cycles([3, 2, 1], base=1)
    assert res.major_index == 3
    assert res.descents == 2
    assert res.inversions == 3
