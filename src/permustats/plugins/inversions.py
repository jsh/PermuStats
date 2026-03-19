from permustats.models import AnalysisResult


class InversionInspector:
    """
    Inspector for Inversion metrics.
    Strictly returns the pre-calculated inversion count.
    """

    def __init__(self) -> None:
        self.name = "inversions"

    def calculate(self, result: AnalysisResult) -> int:
        """Returns the inversion count from the slotted AnalysisResult."""
        return result.inversions
