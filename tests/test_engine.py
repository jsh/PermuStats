import pytest
from permustats.engine import PermuStatsEngine
from permustats.plugins import FixedPointPlugin, CycleLengthsPlugin, CycleCountPlugin
from permustats.transformers import CycleTransformer


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
    plugin = CycleLengthsPlugin()  # This returns [len, len...]
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


def test_p_value_precision():
    engine = PermuStatsEngine(FixedPointPlugin())
    # 2 out of 3 are >= 1.5
    result = engine.calculate_p_value(observed=1.5, permutations=[1.0, 1.5, 2.0])
    assert result == pytest.approx(0.6666667, rel=1e-6)


@pytest.mark.parametrize(
    "permutations, expected",
    [
        ([], 0.0),  # Edge case: Empty
        ([1.0], 1.0),  # Edge case: Singleton (1 >= 1)
        ([0.0], 0.0),  # Edge case: Singleton (0 < 1)
    ],
)
def test_engine_p_value_boundary_conditions(permutations, expected):
    engine = PermuStatsEngine(FixedPointPlugin())
    assert engine.calculate_p_value(1.0, permutations) == expected
