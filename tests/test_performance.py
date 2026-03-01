import pytest
import time
import os
import json
from datetime import datetime

from permustats.generator import PermutationGenerator
from permustats.engine import PermuStatsEngine
from permustats.plugins import FixedPointPlugin


@pytest.mark.skipif(
    not os.getenv("GITHUB_ACTIONS"), reason="Performance tests only run in CI"
)
def test_performance_heavy_sampling(capsys):
    engine = PermuStatsEngine(plugin=FixedPointPlugin())
    start = time.perf_counter()
    # Process 10k permutations
    list(engine.process(PermutationGenerator.sample(10, 10000, rng=engine.rng)))
    end = time.perf_counter()
    print(f"Benchmark took {end - start:.4f}s")
    duration = end - start
    # Create a results dictionary
    results = {
        "timestamp": datetime.now().isoformat(),
        "duration": duration,
        "n": 10,
        "samples": 10000,
        "environment": "GitHub Actions" if os.getenv("GITHUB_ACTIONS") else "Local",
    }

    # Append to a local file
    with open("benchmark_history.jsonl", "a") as f:
        f.write(json.dumps(results) + "\n")


"""
def test_engine_performance_benchmark():
    engine = PermuStatsEngine(plugin=FixedPointPlugin())
    start = time.perf_counter()
    # Process 10k permutations
    list(engine.process(PermutationGenerator.sample(10, 10000, rng=engine.rng)))
    end = time.perf_counter()
    print(f"Benchmark took {end - start:.4f}s")
"""
