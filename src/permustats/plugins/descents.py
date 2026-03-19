from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from permustats.models import AnalysisResult


class DescentPlugin:
    """Extracts the pre-calculated number of descents."""

    def __init__(self) -> None:
        self.name = "descents"

    def calculate(self, result: AnalysisResult) -> int:
        return result.descents
