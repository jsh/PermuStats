import pytest
from generator import PermutationGenerator
from transformers import FixedPointCounter
from engine import PermuStatsEngine

def test_engine_fixed_point_pipeline():
    """
    Verify Exhaustive(3) -> FixedPointCounter produces 
    the expected sequence of counts.
    
    Permutations of N=3 in lexicographic order:
    [0,1,2] -> 3 fixed points
    [0,2,1] -> 1 fixed point
    [1,0,2] -> 1 fixed point
    [1,2,0] -> 0 fixed points
    [2,0,1] -> 0 fixed points
    [2,1,0] -> 1 fixed point
    """
    gen = PermutationGenerator.exhaustive(3)
    counter = FixedPointCounter()
    
    engine = PermuStatsEngine(generator=gen, counter=counter)
    results = engine.run()
    
    # Note: Depending on itertools.permutations exact output order,
    # the sequence should contain exactly these values.
    # [0,1,2]=3, [0,2,1]=1, [1,0,2]=1, [1,2,0]=0, [2,0,1]=0, [2,1,0]=1
    expected = [3, 1, 1, 0, 0, 1] 
    
    # We check that the counts match the distribution required.
    assert sorted(results) == sorted([3, 1, 1, 1, 0, 0])
    assert results == expected
