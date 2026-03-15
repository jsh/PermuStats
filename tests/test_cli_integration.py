from __future__ import annotations
from permustats.main import run_analysis


def test_cli_validation_smoke_test(capsys):
    """
    Automates the manual check: uv run permustats -n 3 --stat cycle-counts --validate
    """
    # Simulate the CLI arguments
    args = ["-n", "3", "--stat", "cycle-counts", "--validate"]

    # Run the analysis
    run_analysis(args)

    # Capture the stdout
    captured = capsys.readouterr().out

    # Assertions to ensure the Validation Tap actually ran and succeeded
    assert "🛡️ Validation Report" in captured
    assert "Samples Processed: 6" in captured
    assert "✅ Mean Cycles (H_n)" in captured
    assert "✅ Mean Fixed Points" in captured
    # Ensure no warnings were triggered
    assert "⚠️" not in captured
