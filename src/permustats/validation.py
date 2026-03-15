from __future__ import annotations

import json
import math
import os
from typing import TYPE_CHECKING, Any

import requests

from permustats.math_utils import harmonic_number

if TYPE_CHECKING:
    from permustats.analysis import AnalysisResult


def validate_results(n: int, distribution: dict[int, int]) -> bool:
    """Verifies dē rēbus mathematicīs: Sum(freq) = n! and E[X] = 1."""
    n_factorial = math.factorial(n)
    total_count = sum(distribution.values())
    weighted_sum = sum(val * freq for val, freq in distribution.items())
    return total_count == n_factorial and weighted_sum == n_factorial


class OEISLookup:
    _cache_file = "oeis_cache.json"

    @staticmethod
    def format_sequence(n: int, distribution: dict[int | float, int]) -> str:
        """
        Converts distribution to 'val0,val1,val2...' string.

        Keys are converted to integers to ensure they can index the 0..n range.
        """
        return ",".join(str(distribution.get(int(i), 0)) for i in range(n + 1))

    @classmethod
    def search(cls, sequence_str: str) -> dict[str, str] | None:
        """
        Queries OEIS with a local JSON cache to prevent redundant API hits.
        Returns a dict with 'id' and 'name' or None.
        """
        cache = cls._load_cache()
        if sequence_str in cache:
            return cache[sequence_str]

        url = f"https://oeis.org/search?q={sequence_str}&fmt=json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Handle case where data is a list or a dict containing 'results'
            results = data if isinstance(data, list) else data.get("results", [])

            if results:
                # results[0] is the top match
                first_match = results[0]
                result = {
                    "id": f"A{first_match['number']:06d}",
                    "name": first_match["name"],
                }
                cache[sequence_str] = result
                cls._save_cache(cache)
                return result
        except (requests.exceptions.RequestException, KeyError, IndexError, TypeError):
            # Sī rēs male cecidit... (If things fell badly...)
            return None

        return None

    @classmethod
    def _load_cache(cls) -> dict[str, Any]:
        if os.path.exists(cls._cache_file):
            try:
                with open(cls._cache_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    @classmethod
    def _save_cache(cls, cache: dict[str, Any]) -> None:
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
        self.length_counts: dict[int, int] = {}

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

        # Use tighter tolerance if we've seen a large enough sample
        tol = 0.01 if self.count > 500 else 0.05

        self._print_metric("Mean Cycles (H_n)", expected_harmonic, obs_mean_cycles, tol)
        self._print_metric("Mean Fixed Points", 1.0, obs_mean_fixed, tol)

        print("\nCycle Length Distribution (1/k Rule):")
        for k in range(1, self.n + 1):
            expected_k = 1.0 / k
            actual_k = self.length_counts.get(k, 0) / self.count
            self._print_metric(f"  Length k={k}", expected_k, actual_k, tol)

    def _print_metric(self, name: str, expected: float, actual: float, tol: float):
        """Helper to print with tolerance check."""
        is_valid = math.isclose(expected, actual, rel_tol=tol)
        status = "✅" if is_valid else "⚠️"
        print(f"{status} {name:20} | Expected: {expected:.4f} | Actual: {actual:.4f}")
