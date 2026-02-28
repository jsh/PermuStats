import itertools
import random


class PermutationGenerator:
    """Core logic for generating lexicographic and random permutations."""

    @staticmethod
    def exhaustive(n):
        """Yields all permutations of size N in lexicographic order."""
        elements = list(range(n))
        for p in itertools.permutations(elements):
            yield list(p)

    @staticmethod
    def sample(n, num_samples):
        """Yields num_samples random permutations of size N."""
        elements = list(range(n))
        for _ in range(num_samples):
            # random.sample is perfect here to ensure no repeats within the list
            yield random.sample(elements, n)
