import pytest
from engine import PermuStatsEngine
from plugins import FixedPointPlugin, CycleLengthPlugin
from transformers import CycleTransformer

def test_engine_with_fixed_points():
    # No transformer needed for fixed points
    plugin = FixedPointPlugin()
    engine = PermuStatsEngine(plugin)
    
    data = [[0, 1, 2], [1, 0, 2]]
    results = list(engine.process(data))
    
    assert results == [3, 1]

def test_engine_with_cycle_lengths():
    # Needs CycleTransformer to turn [1, 0, 2] into [[0, 1], [2]]
    plugin = CycleLengthPlugin()
    transformer = CycleTransformer()
    engine = PermuStatsEngine(plugin, transformer)
    
    data = [[1, 0, 2]] # This is a list of permutations
    results = list(engine.process(data))
    
    # [1, 0, 2] becomes 2 cycles -> [[0, 1], [2]] -> plugin returns 2
    assert results == [2]

def test_engine_streaming():
    """Verify engine handles generators (streams) correctly."""
    engine = PermuStatsEngine(FixedPointPlugin())
    
    def stream():
        yield [0, 1, 2]
        yield [1, 0, 2]
        
    results = list(engine.process(stream()))
    assert len(results) == 2
