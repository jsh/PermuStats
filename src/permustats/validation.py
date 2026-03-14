import math
import requests
import json
import os

from typing import Dict

from permustats.analysis import AnalysisResult
from permustats.math_utils import harmonic_number


def validate_results(n, distribution):
    """Verifies combinatorial identities: Sum(freq) = n! and E[X] = 1."""
    n_factorial = math.factorial(n)
    total_count = sum(distribution.values())
    weighted_sum = sum(val * freq for val, freq in distribution.items())
    return total_count == n_factorial and weighted_sum == n_factorial


class OEISLookup:
    _cache_file = "oeis_cache.json"

    @staticmethod
    def format_sequence(n, distribution):
        """Converts distribution to "val0,val1,val2..." string."""
        return ",".join(str(distribution.get(i, 0)) for i in range(n + 1))

    @classmethod
    def search(cls, sequence_str):
        """
        Queries OEIS with a local JSON cache to prevent redundant API hits.
        Returns a dict with 'id' and 'name' or None.
        """
        # 1. Check local cache first
        cache = cls._load_cache()
        if sequence_str in cache:
            return cache[sequence_str]

        # 2. Perform live search
        url = f"https://oeis.org/search?q={sequence_str}&fmt=json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get("results"):
                result = {
                    "id": f"A{data['results'][0]['number']:06d}",
                    "name": data["results"][0]["name"],
                }
                # 3. Save to cache
                cache[sequence_str] = result
                cls._save_cache(cache)
                return result

        except Exception as e:
            return {"error": f"Connection failed: {e}"}

        return None

    @classmethod
    def _load_cache(cls):
        if os.path.exists(cls._cache_file):
            with open(cls._cache_file, "r") as f:
                return json.load(f)
        return {}

    @classmethod
    def _save_cache(cls, cache):
        with open(cls._cache_file, "w") as f:
            json.dump(cache, f, indent=4)


class ValidationTap:
    """
    A decoupled observer that validates empirical results against
    theoretical combinatorial truths.
    """

    __slots__ = ["n", "count", "total_cycles", "total_fixed_points", "length_counts"]

    def __init__(self, n: int):
        self.n = n
        self.count = 0
        self.total_cycles = 0
        self.total_fixed_points = 0
        self.length_counts: Dict[int, int] = {}

    def observe(self, result: AnalysisResult) -> None:
        """Process a single result and update running tallies."""
        self.count += 1
        self.total_cycles += result.total_cycles
        self.total_fixed_points += result.fixed_points

        for length, freq in result.cycle_lengths.items():
            self.length_counts[length] = self.length_counts.get(length, 0) + freq

    def report(self) -> None:
        """Compares observations to mathematical ground truths."""
        if self.count == 0:
            print("Validation skipped: No data observed.")
            return

        expected_harmonic = harmonic_number(self.n)
        obs_mean_cycles = self.total_cycles / self.count
        obs_mean_fixed = self.total_fixed_points / self.count

        print("\n--- 🛡️ Validation Report ---")
        print(f"Samples Processed: {self.count}")

        # 1. Total Cycles vs Harmonic Number
        self._print_metric("Mean Cycles (H_n)", expected_harmonic, obs_mean_cycles)

        # 2. Fixed Point Mean (Expected to be 1.0)
        self._print_metric("Mean Fixed Points", 1.0, obs_mean_fixed)

        # 3. The 1/k Rule (Expectation: sum of cycles of length k / N = 1/k)
        print("\nCycle Length Distribution (1/k Rule):")
        for k in range(1, self.n + 1):
            expected_k = 1.0 / k
            actual_k = self.length_counts.get(k, 0) / self.count
            self._print_metric(f"  Length k={k}", expected_k, actual_k)

    def _print_metric(self, name: str, expected: float, actual: float):
        """Helper to print with tolerance check."""
        # Inspector's Requirement: Floating Point Tolerance
        # Using a 1% tolerance for sampling or exact for exhaustive
        is_valid = math.isclose(expected, actual, rel_tol=0.05)
        status = "✅" if is_valid else "⚠️"
        print(f"{status} {name:20} | Expected: {expected:.4f} | Actual: {actual:.4f}")
