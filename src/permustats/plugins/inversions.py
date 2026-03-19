from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from permustats.models import AnalysisResult


class InversionPlugin:
    """Extracts the pre-calculated inversion count."""

    def __init__(self) -> None:
        self.name = "inversions"

    def calculate(self, result: AnalysisResult) -> int:
        return result.inversions
