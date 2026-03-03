from abc import ABC, abstractmethod
from typing import Any


class PermuPlugin(ABC):
    @abstractmethod
    def calculate(self, data: Any) -> Any:
        """Abstract method for calculating a statistic from permutation data."""
        pass


class FixedPointPlugin(PermuPlugin):
    """Returns the number of fixed points in a permutation (int)."""

    def calculate(self, data: list[int]) -> int:
        return sum(1 for i, val in enumerate(data) if i == val)


class CycleCountPlugin(PermuPlugin):
    """Returns the total number of cycles (int)."""

    def calculate(self, data: list[list[int]]) -> int:
        return len(data)


class CycleLengthsPlugin(PermuPlugin):
    """Returns a list of the lengths of each cycle (list[int])."""

    def calculate(self, data: list[list[int]]) -> list[int]:
        return [len(c) for c in data]
