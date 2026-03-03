import random
import itertools
from typing import Iterator


class PermutationGenerator:
    """Provides memory-efficient streams of permutations."""

    @staticmethod
    def sample(n: int, num_samples: int, rng: random.Random) -> Iterator[list[int]]:
        """Yield NUM_SAMPLES random permutations of size N (1 to N)."""
        # Shift to 1-indexed to match statistical standards
        elements = list(range(1, n + 1))
        for _ in range(num_samples):
            yield rng.sample(elements, n)

    @staticmethod
    def exhaustive(n: int) -> Iterator[list[int]]:
        """Yield all permutations of size N (1 to N) in lexicographic order."""
        # Shift to 1-indexed
        for p in itertools.permutations(range(1, n + 1)):
            yield list(p)
