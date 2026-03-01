import pytest
import time
import os

from permustats.generator import PermutationGenerator
from permustats.engine import PermuStatsEngine
from permustats.plugins import FixedPointPlugin


@pytest.mark.skipif(
    not os.getenv("GITHUB_ACTIONS"), reason="Performance tests only run in CI"
)
def test_engine_performance_benchmark():
    engine = PermuStatsEngine(plugin=FixedPointPlugin())
    start = time.perf_counter()
    # Process 10k permutations
    list(engine.process(PermutationGenerator.sample(10, 10000, rng=engine.rng)))
    end = time.perf_counter()
    print(f"Benchmark took {end - start:.4f}s")
