import pytest
from unittest.mock import MagicMock, patch
from permustats.analysis import Analyzer
from permustats.models import AnalysisResult


def create_mock_result(descents: int) -> AnalysisResult:
    """Helper to satisfy the strict AnalysisResult dataclass requirements."""
    return AnalysisResult(
        permutation=[1, 2, 3],  # Changed tuple to list
        cycles=[[1], [2], [3]],  # Changed tuples to lists
        total_cycles=3,
        fixed_points=3,
        lengths_sequence=[1, 1, 1],  # Changed tuple to list
        cycle_lengths={1: 3},
        inversions=0,
        descents=descents,
        exceedances=0,
        major_index=0,
    )


@pytest.fixture
def sample_results():
    # N=3 descents distribution: {0: 1, 1: 4, 2: 1}
    return [
        create_mock_result(0),
        create_mock_result(1),
        create_mock_result(1),
        create_mock_result(1),
        create_mock_result(1),
        create_mock_result(2),
    ]


def test_plot_raises_runtime_error_when_matplotlib_missing(sample_results):
    """Verify that we give a helpful error if the 'plot' extra isn't installed."""
    analyzer = Analyzer(sample_results)

    # Force the plt-is-None state
    with patch("permustats.analysis.plt", None):
        with pytest.raises(RuntimeError) as excinfo:
            analyzer.plot("descents")
        assert "Install it with: pip install 'permustats[plot]'" in str(excinfo.value)


def test_plot_calls_matplotlib_correctly(sample_results):
    """Verify that the data is passed to plt.bar in sorted order."""
    analyzer = Analyzer(sample_results)

    # Mock plt to avoid opening windows during tests
    mock_plt = MagicMock()
    with patch("permustats.analysis.plt", mock_plt):
        analyzer.plot("descents")

        # Check if plt.bar was called with sorted keys and correct frequencies
        # Expected: x=[0, 1, 2], y=[1, 4, 1]
        args, kwargs = mock_plt.bar.call_args
        assert list(args[0]) == [0, 1, 2]
        assert list(args[1]) == [1, 4, 1]

        # Verify labeling occurred
        mock_plt.title.assert_called()
        mock_plt.xlabel.assert_called_with("Descents")


def test_plot_with_save_path(sample_results):
    """Verify plt.savefig is used when a path is provided."""
    analyzer = Analyzer(sample_results)
    mock_plt = MagicMock()

    with patch("permustats.analysis.plt", mock_plt):
        analyzer.plot("descents", save_path="test_plot.png")
        mock_plt.savefig.assert_called_with("test_plot.png")
        # Ensure show() was NOT called if saving
        mock_plt.show.assert_not_called()


def test_plot_saves_to_file(sample_results, tmp_path):
    """Verify that providing a save_path triggers plt.savefig."""
    analyzer = Analyzer(sample_results)
    mock_plt = MagicMock()

    # Use a temporary directory provided by pytest
    save_file = tmp_path / "distribution.png"

    with patch("permustats.analysis.plt", mock_plt):
        analyzer.plot("descents", save_path=str(save_file))

        # Verify savefig was called with our path
        mock_plt.savefig.assert_called_once_with(str(save_file))
        # CRITICAL: show() must NOT be called if we are saving to a file
        mock_plt.show.assert_not_called()
