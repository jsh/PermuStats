import pytest
from plugins import FixedPointPlugin, CycleCountPlugin, CycleLengthsPlugin, PermuPlugin

def test_fixed_point_plugin():
    plugin = FixedPointPlugin()
    # [0, 1, 2] has 3 fixed points
    assert plugin.calculate([0, 1, 2]) == 3
    # [1, 0, 2] has 1 fixed point (index 2)
    assert plugin.calculate([1, 0, 2]) == 1
    # [1, 2, 0] has 0 fixed points
    assert plugin.calculate([1, 2, 0]) == 0

def test_cycle_count_plugin():
    plugin = CycleCountPlugin()
    # Expects list of lists (cycles)
    # One giant cycle: [[0, 1, 2]] -> count is 1
    assert plugin.calculate([[0, 1, 2]]) == 1
    # Three individual cycles: [[0], [1], [2]] -> count is 3
    assert plugin.calculate([[0], [1], [2]]) == 3
    # [[0, 1], [2]] -> 2 cycles
    assert plugin.calculate([[0, 1], [2]]) == 2


def test_cycle_lengths_plugin():
    plugin = CycleLengthsPlugin()
    # [[0, 1], [2]] -> cycle lengths of 2 and 1
    result = plugin.calculate([[0, 1], [2]])
    assert result == [2, 1]

def test_permu_plugin_is_abstract():
    with pytest.raises(TypeError):
        # This should fail because PermuPlugin has abstract methods
        _ = PermuPlugin()
