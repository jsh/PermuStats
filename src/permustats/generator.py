import random
import itertools
from typing import Iterator


class PermutationGenerator:
    """Provides memory-efficient streams of permutations."""

    @staticmethod
    def sample(n: int, num_samples: int, rng: random.Random) -> Iterator[list[int]]:
        """Yield NUM_SAMPLES random permutations of size N using a specific seeded RNG."""
        elements = list(range(n))
        for _ in range(num_samples):
            # Crucial: use the passed rng instance, not global random
            yield rng.sample(elements, n)

    @staticmethod
    def exhaustive(n: int) -> Iterator[list[int]]:
        """Yield all permutations of size N in lexicographic order (the exact approach)."""
        for p in itertools.permutations(range(n)):
            yield list(p)
