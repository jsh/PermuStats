from permustats.engine import PermuStatsEngine
from permustats.plugins import FixedPointPlugin


def test_engine_determinism():
    """Verify that identical seeds produce identical p-values."""
    seed = 42
    n, samples = 10, 100

    # Run 1
    engine1 = PermuStatsEngine(plugin=FixedPointPlugin(), seed=seed)
    results1 = list(engine1.run_study(n=n, num_samples=samples))

    # Run 2
    engine2 = PermuStatsEngine(plugin=FixedPointPlugin(), seed=seed)
    results2 = list(engine2.run_study(n=n, num_samples=samples))

    assert results1 == results2, "Seeded runs should be identical."


def test_engine_randomness():
    """Verify that different seeds (or no seed) produce different results."""
    n, samples = 10, 100

    engine1 = PermuStatsEngine(plugin=FixedPointPlugin(), seed=1)
    results1 = list(engine1.run_study(n=n, num_samples=samples))

    engine2 = PermuStatsEngine(plugin=FixedPointPlugin(), seed=2)
    results2 = list(engine2.run_study(n=n, num_samples=samples))

    assert results1 != results2, "Different seeds should produce different samples."
