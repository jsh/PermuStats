import pytest
from plugins import FixedPointPlugin, CycleLengthPlugin

def test_fixed_point_plugin():
    plugin = FixedPointPlugin()
    # [0, 1, 2] has 3 fixed points
    assert plugin.calculate([0, 1, 2]) == 3
    # [1, 0, 2] has 1 fixed point (index 2)
    assert plugin.calculate([1, 0, 2]) == 1
    # [1, 2, 0] has 0 fixed points
    assert plugin.calculate([1, 2, 0]) == 0

def test_cycle_length_plugin():
    plugin = CycleLengthPlugin()
    # Expects list of lists (cycles)
    # One giant cycle: [[0, 1, 2]] -> count is 1
    assert plugin.calculate([[0, 1, 2]]) == 1
    # Three individual cycles: [[0], [1], [2]] -> count is 3
    assert plugin.calculate([[0], [1], [2]]) == 3
