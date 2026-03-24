from unittest.mock import patch
from permustats.main import run_analysis


def test_cli_passes_save_path_to_analyzer():
    """
    Verify that the CLI takes -o and passes it to analyzer.plot().
    We configure the mock to return actual floats to satisfy f-string formatting.
    """
    test_args = ["-n", "3", "--stat", "inversions", "-o", "my_plot.png"]

    with patch("permustats.main.Analyzer") as MockAnalyzer:
        # Get the instance that the class returns
        mock_instance = MockAnalyzer.return_value

        # Configure methods to return primitive floats
        mock_instance.mean.return_value = 0.0
        mock_instance.variance.return_value = 0.0
        mock_instance.frequency_distribution.return_value = {0: 1}

        # Manually set the _count attribute to a primitive int
        mock_instance._count = 1

        # Run the CLI entry point
        run_analysis(test_args)

        # Check that plot was called with the correct arguments
        mock_instance.plot.assert_called_once_with(
            "inversions", save_path="my_plot.png"
        )
