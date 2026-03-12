class CycleTransformer:
    def transform(self, p: list[int]):
        """Converts a 1-indexed permutation to canonical cycle form."""
        n = len(p)
        visited = [False] * n
        cycles = []

        # Pre-map the permutation to 0-indexed pointers for the jump logic
        # [1, 2, 3] becomes [0, 1, 2]
        adj_p = [x - 1 for x in p]

        for i in range(n):
            if not visited[i]:
                curr = i
                cycle = []
                while not visited[curr]:
                    visited[curr] = True
                    cycle.append(
                        p[curr]
                    )  # Keep the original 1-indexed value for the cycle
                    curr = adj_p[curr]  # Jump using the 0-indexed map
                cycles.append(cycle)
        return cycles
