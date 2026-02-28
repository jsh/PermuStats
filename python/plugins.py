from abc import ABC, abstractmethod


class PermuPlugin(ABC):
    @abstractmethod
    def calculate(self, data):
        pass


class FixedPointPlugin(PermuPlugin):
    """Expects a raw permutation (List[int])."""

    def calculate(self, p):
        return sum(1 for i, val in enumerate(p) if i == val)


class CycleCountPlugin(PermuPlugin):
    """Returns the total number of cycles (int)."""

    def calculate(self, cycles):
        return int(len(cycles))  # Explicit int casting just to be safe


class CycleLengthsPlugin(PermuPlugin):
    """Returns a list of the lengths of each cycle (List[int])."""

    def calculate(self, cycles):
        return [len(c) for c in cycles]
