from __future__ import annotations

import dataclasses
from typing import Optional


@dataclasses.dataclass
class OEISMatch:
    id: str
    name: str


class OEISLookup:
    """The bridge between PermuStats and the Online Encyclopedia of Integer Sequences."""

    def __init__(self) -> None:
        # Local cache of key combinatorial distributions
        # Format: "count_at_val_0,count_at_val_1,..."
        self._cache: dict[str, OEISMatch] = {
            # N=3 Stirling numbers (1st kind): [2, 3, 1] for cycles 1, 2, 3
            "2,3,1": OEISMatch("A008275", "Stirling numbers of first kind"),
            # N=4 Stirling numbers (1st kind): [6, 11, 6, 1]
            "6,11,6,1": OEISMatch("A008275", "Stirling numbers of first kind"),
            # N=3 Eulerian (Descents): [1, 4, 1]
            "1,4,1": OEISMatch("A008292", "Eulerian numbers T(n, k)"),
            # N=4 Eulerian (Descents): [1, 11, 11, 1]
            "1,11,11,1": OEISMatch("A008292", "Eulerian numbers T(n, k)"),
            # N=3 Mahonian (Inversions): [1, 2, 2, 1]
            "1,2,2,1": OEISMatch("A008302", "Mahonian numbers (Inversions)"),
            # N=4 Mahonian (Inversions): [1, 3, 5, 6, 5, 3, 1]
            "1,3,5,6,5,3,1": OEISMatch("A008302", "Mahonian numbers (Inversions)"),
        }

    def search(self, sequence_str: str) -> Optional[OEISMatch]:
        """Search for a comma-separated frequency distribution."""
        return self._cache.get(sequence_str)
