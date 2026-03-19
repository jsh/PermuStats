from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from .descents import DescentPlugin
from .inversions import InversionPlugin
from .major_index import MajorIndexPlugin

# Ensure it's in __all__ if you use that pattern
__all__ = [
    "DescentPlugin",
    "FixedPointPlugin",
    "CycleCountPlugin",
    "CycleLengthsPlugin",
    "InversionPlugin",
    "MajorIndexPlugin",
]

if TYPE_CHECKING:
    from permustats.models import AnalysisResult


class PermuPlugin(ABC):
    @abstractmethod
    def calculate(self, result: AnalysisResult) -> Any:
        """Calculates a statistic by extracting data from an AnalysisResult."""
        pass


class FixedPointPlugin(PermuPlugin):
    """Extracts the pre-calculated number of fixed points."""

    def calculate(self, result: AnalysisResult) -> int:
        return result.fixed_points


class CycleCountPlugin(PermuPlugin):
    """Extracts the total number of cycles."""

    def calculate(self, result: AnalysisResult) -> int:
        return result.total_cycles


class CycleLengthsPlugin(PermuPlugin):
    """Extracts the sequence of cycle lengths."""

    def calculate(self, result: AnalysisResult) -> list[int]:
        return result.lengths_sequence
