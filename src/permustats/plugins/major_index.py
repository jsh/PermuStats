from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from permustats.models import AnalysisResult


class MajorIndexPlugin:
    """Extracts the pre-calculated Major Index."""

    def __init__(self) -> None:
        self.name = "major_index"

    def calculate(self, result: AnalysisResult) -> int:
        return result.major_index
