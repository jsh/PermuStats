from abc import ABC, abstractmethod

class PermuPlugin(ABC):
    @abstractmethod
    def calculate(self, data):
        pass

class FixedPointPlugin(PermuPlugin):
    """Expects a raw permutation (List[int])."""
    def calculate(self, p):
        return sum(1 for i, val in enumerate(p) if i == val)

class CycleLengthPlugin(PermuPlugin):
    """Expects cycle-form data (List[List[int]]). Returns number of cycles."""
    def calculate(self, cycles):
        return len(cycles)
