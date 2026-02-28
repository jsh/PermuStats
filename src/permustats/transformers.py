class CycleTransformer:
    def transform(self, p):
        """Converts a permutation list to canonical cycle form (list of lists)."""
        n = len(p)
        visited = [False] * n
        cycles = []
        for i in range(n):
            if not visited[i]:
                curr = i
                cycle = []
                while not visited[curr]:
                    visited[curr] = True
                    cycle.append(curr)
                    curr = p[curr]
                cycles.append(cycle)
        return cycles
