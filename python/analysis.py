import statistics

class Analyzer:
    def __init__(self, results):
        """Cast to list to allow multiple statistical passes"""
        self.results = list(results)

    def mean(self):
        """Returns the average number of fixed points (Expected value is 1)."""
        return statistics.mean(self.results) if self.results else 0

    def variance(self):
        """Using population variance (pvariance) for exhaustive sets"""
        return statistics.pvariance(self.results) if self.results else 0

    def frequency_distribution(self):
        """Returns a dictionary mapping each fixed-point count to its frequency."""
        dist = {}
        for val in self.results:
            dist[val] = dist.get(val, 0) + 1
        return dist
