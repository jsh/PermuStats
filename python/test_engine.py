import pytest
from engine import PermuStatsEngine
from plugins import FixedPointPlugin, CycleLengthsPlugin, CycleCountPlugin
from transformers import CycleTransformer

def test_engine_with_fixed_points():
    # No transformer needed for fixed points
    plugin = FixedPointPlugin()
    engine = PermuStatsEngine(plugin)
    
    data = [[0, 1, 2], [1, 0, 2]]
    results = list(engine.process(data))
    
    assert results == [3, 1]

def test_engine_streaming():
    """Verify engine handles generators (streams) correctly."""
    engine = PermuStatsEngine(FixedPointPlugin())
    
    def stream():
        yield [0, 1, 2]
        yield [1, 0, 2]
        
    results = list(engine.process(stream()))
    assert len(results) == 2

def test_engine_with_cycle_lengths():
    plugin = CycleLengthsPlugin() # This returns [len, len...]
    transformer = CycleTransformer()
    engine = PermuStatsEngine(plugin, transformer)

    data = [[1, 0, 2]] 
    results = list(engine.process(data))

    # [1, 0, 2] -> cycles [[0, 1], [2]] -> lengths [2, 1]
    assert results == [[2, 1]] 

def test_engine_with_cycle_counts():
    # If you want to test for the scalar '2', use the Count plugin
    plugin = CycleCountPlugin()
    transformer = CycleTransformer()
    engine = PermuStatsEngine(plugin, transformer)
    
    data = [[1, 0, 2]]
    results = list(engine.process(data))
    assert results == [2]
