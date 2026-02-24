class PermuStatsEngine:
    """Wires together generators, transformers, and a counter to produce data."""

    def __init__(self, generator, counter, transformers=None):
        """
        :param generator: A Python generator yielding lists (permutations).
        :param counter: A PermuPlugin that returns a numerical result.
        :param transformers: (Optional) A list of PermuPlugins to transform the data first.
        """
        self.generator = generator
        self.counter = counter
        self.transformers = transformers or []

    def run(self) -> list:
        """Processes all permutations through the pipeline and returns the results."""
        results = []
        
        for p in self.generator:
            data = p
            # Pass the data through each transformer in the chain
            for transformer in self.transformers:
                data = transformer.process(data)
            
            # Extract the final statistic
            results.append(self.counter.process(data))
            
        return results
