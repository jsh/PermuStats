class PermuStatsEngine:
    def __init__(self, plugin, transformer=None):
        self.plugin = plugin
        self.transformer = transformer

    def process(self, data_stream):
        """Processes each permutation through a transformer (if any) then the plugin."""
        for p in data_stream:
            processed_data = p
            if self.transformer:
                processed_data = self.transformer.transform(p)
            
            yield self.plugin.calculate(processed_data)
