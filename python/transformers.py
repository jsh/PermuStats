from plugin import PermuPlugin

class CycleFormTransformer(PermuPlugin):
    """Converts a permutation to its Canonical Cycle Form."""

    def process(self, permutation: list[int]) -> list[list[int]]:
        n = len(permutation)
        visited = [False] * n
        cycles = []

        for i in range(n):
            if not visited[i]:
                # Start a new cycle
                curr_cycle = []
                curr_idx = i
                
                while not visited[curr_idx]:
                    visited[curr_idx] = True
                    curr_cycle.append(curr_idx)
                    # Move to the element this index points to
                    curr_idx = permutation[curr_idx]
                
                cycles.append(curr_cycle)
        
        return cycles

class FixedPointCounter(PermuPlugin):
    """Counts elements that map to themselves: p[i] == i."""
    
    def process(self, permutation: list[int]) -> int:
        return sum(1 for i, val in enumerate(permutation) if i == val)


class CycleLengthCounter(PermuPlugin):
    """
    Takes the output of CycleFormTransformer and returns 
     a list of lengths of the cycles.
    """
    
    def process(self, cycles: list[list[int]]) -> list[int]:
        # Simple list comprehension to get the length of each nested list
        return [len(cycle) for cycle in cycles]
