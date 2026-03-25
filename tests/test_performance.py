import pytest
import time
import os
import json
from datetime import datetime, timezone

from permustats.generator import PermutationGenerator
from permustats.engine import PermuStatsEngine
from permustats.plugins import FixedPointPlugin
from permustats.analysis import decompose_cycles

# Change the skip logic and the environment tag
is_ci = os.getenv("GITHUB_ACTIONS") == "true"
is_forced = os.getenv("FORCE_PERF") == "true"


@pytest.mark.skipif(not (is_ci or is_forced), reason="Performance test")
def test_performance_heavy_sampling():
    engine = PermuStatsEngine(plugin=FixedPointPlugin())
    env_name = "GitHub Runner" if is_ci else "Local Laptop"
    start = time.perf_counter()
    # Process 10k permutations
    list(engine.process(PermutationGenerator.sample(10, 10000, rng=engine.rng)))
    end = time.perf_counter()
    print(f"Benchmark took {end - start:.4f}s")
    duration = end - start
    # Create a results dictionary
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),  # Forced UTC
        "duration": duration,
        "n": 10,
        "samples": 10000,
        "environment": env_name,
    }

    # Append to a local file
    with open("benchmark_history.jsonl", "a") as f:
        f.write(json.dumps(results) + "\n")


def test_inversion_complexity_scaling():
    """
    TDD Performance Gate:
    Doubling N from 500 to 1000.
    O(N^2) should take ~4x longer.
    O(N log N) should take ~2.2x longer.
    """
    n1, n2 = 500, 1000
    p1 = list(range(n1, 0, -1))  # Worst case (fully reversed)
    p2 = list(range(n2, 0, -1))

    # Measure N=500
    start = time.perf_counter()
    decompose_cycles(p1)
    time_n1 = time.perf_counter() - start

    # Measure N=1000
    start = time.perf_counter()
    decompose_cycles(p2)
    time_n2 = time.perf_counter() - start

    ratio = time_n2 / time_n1

    print(f"\nScaling Factor (N=500 to 1000): {ratio:.2f}x")

    # This assertion will fail once we optimize,
    # helping us prove the complexity shift.
    assert ratio < 3.0, f"Complexity looks quadratic! Ratio was {ratio:.2f}x"
