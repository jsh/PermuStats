import pytest
from permustats.engine import PermuStatsEngine
from permustats.plugins.descents import DescentPlugin
from permustats.analysis import Analyzer
from permustats.math_utils import eulerian


def test_exhaustive_eulerian_n4():
    """Verify exhaustive distribution for N=4 matches Eulerian row: (1, 11, 11, 1)."""
    n = 4
    plugin = DescentPlugin()
    engine = PermuStatsEngine(plugin=plugin, base=1)

    # Run exhaustive study
    results = engine.run_study(n=n)
    analyzer = Analyzer(results)

    dist = analyzer.frequency_distribution("descents")

    # Eulerian numbers A(4, k) for k = 0, 1, 2, 3
    expected = {0: 1, 1: 11, 2: 11, 3: 1}

    for k, count in expected.items():
        assert dist.get(k, 0) == count, (
            f"A(4, {k}) should be {count}, got {dist.get(k, 0)}"
        )


def test_stochastic_descent_mean_n100():
    """Verify stochastic mean for N=100 is (n-1)/2 = 49.5."""
    n = 100
    samples = 5000
    plugin = DescentPlugin()
    engine = PermuStatsEngine(plugin=plugin, base=1)

    results = engine.run_study(n=n, num_samples=samples)
    analyzer = Analyzer(results)

    expected_mean = (n - 1) / 2
    # 5k samples should easily get within 2% of 49.5
    assert analyzer.mean("descents") == pytest.approx(expected_mean, rel=0.02)


def test_eulerian_symmetry_n6():
    """Check math utility symmetry: A(n, k) == A(n, n-1-k)."""
    n = 6
    for k in range(n):
        assert eulerian(n, k) == eulerian(n, n - 1 - k)
