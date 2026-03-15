from __future__ import annotations
from permustats.analysis import decompose_cycles
from permustats.plugins import FixedPointPlugin, CycleCountPlugin, CycleLengthsPlugin


def test_fixed_point_plugin():
    plugin = FixedPointPlugin()
    # Use decompose_cycles to create the rich object the plugin now expects
    res1 = decompose_cycles([1, 2, 3], base=1)  # 3 fixed points
    assert plugin.calculate(res1) == 3

    res2 = decompose_cycles([2, 1, 3], base=1)  # 1 fixed point (3)
    assert plugin.calculate(res2) == 1


def test_cycle_count_plugin():
    plugin = CycleCountPlugin()
    # One giant cycle: (1 2 3)
    res1 = decompose_cycles([2, 3, 1], base=1)
    assert plugin.calculate(res1) == 1

    # Three individual cycles: (1)(2)(3)
    res2 = decompose_cycles([1, 2, 3], base=1)
    assert plugin.calculate(res2) == 3


def test_cycle_lengths_plugin():
    plugin = CycleLengthsPlugin()
    # (1 2)(3) -> cycle lengths of 2 and 1
    res = decompose_cycles([2, 1, 3], base=1)
    assert plugin.calculate(res) == [2, 1]
