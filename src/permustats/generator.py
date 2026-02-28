import itertools
import random
from typing import Iterator, List


class PermutationGenerator:
    """Provides memory-efficient streams of permutations."""

    @staticmethod
    def exhaustive(n: int) -> Iterator[List[int]]:
        """Yields all permutations of size N in lexicographic order."""
        elements: List[int] = list(range(n))
        for p in itertools.permutations(elements):
            yield list(p)

    @staticmethod
    def sample(n: int, num_samples: int) -> Iterator[List[int]]:
        """Yields num_samples random permutations of size N."""
        elements: List[int] = list(range(n))
        for _ in range(num_samples):
            # random.sample returns a new list
            yield random.sample(elements, n)
