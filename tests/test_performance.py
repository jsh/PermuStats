import pytest
import time
import os
import json
from datetime import datetime, timezone

from permustats.generator import PermutationGenerator
from permustats.engine import PermuStatsEngine
from permustats.plugins import FixedPointPlugin

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
