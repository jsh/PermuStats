import statistics


class Analyzer:
    def __init__(self, results):
        self.results = list(results)

    def mean(self):
        # Only calculate mean for numeric results (ints/floats)
        # If results are lists/tuples, mean isn't mathematically defined here
        try:
            return statistics.mean(self.results) if self.results else 0
        except TypeError:
            return 0.0

    def variance(self):
        try:
            return statistics.pvariance(self.results) if self.results else 0
        except TypeError:
            return 0.0

    def frequency_distribution(self):
        dist = {}
        for val in self.results:
            # ONLY tuple-ify if it's a list. If it's an int, leave it alone!
            key = tuple(val) if isinstance(val, list) else val
            dist[key] = dist.get(key, 0) + 1
        return dist
