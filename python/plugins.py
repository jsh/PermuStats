class FixedPointPlugin:
    """Expects a raw permutation (List[int])."""
    def calculate(self, p):
        return sum(1 for i, val in enumerate(p) if i == val)

class CycleLengthPlugin:
    """Expects cycle-form data (List[List[int]]). Returns number of cycles."""
    def calculate(self, cycles):
        return len(cycles)
