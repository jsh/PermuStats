from abc import ABC, abstractmethod

class PermuPlugin(ABC):
    """Abstract Base Class for all PermuStats plugins."""

    @abstractmethod
    def process(self, permutation: list[int]):
        """
        Processes a permutation and returns a result.
        Must be implemented by subclasses.
        """
        pass
