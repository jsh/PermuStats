import pytest
from permustats.engine import PermuStatsEngine
from permustats.analysis import Analyzer


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


def test_major_index_specific_case():
    """Manual check for a known permutation: [3, 2, 1]."""
    from permustats.analysis import decompose_cycles

    # [3, 2, 1] base 1
    # Descent at pos 1: 3 > 2
    # Descent at pos 2: 2 > 1
    # Maj = 1 + 2 = 3
    res = decompose_cycles([3, 2, 1], base=1)
    assert res.major_index == 3
    assert res.descents == 2
    assert res.inversions == 3
