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


def test_cli_cycle_counts_stirling_identity(capsys):
    """
    Integration Test: Verify N=3 cycle-counts returns Stirling Numbers (A008275).
    Distribution for S_3 cycle counts: {1: 2, 2: 3, 3: 1}
    """
    # Simulate: python -m permustats.main -n 3 --stat cycle-counts
    args = ["-n", "3", "--stat", "cycle-counts"]

    run_analysis(args)
    captured = capsys.readouterr().out

    # 1. Verify the Header and Statistics
    assert "--- Statistics Report [total_cycles] ---" in captured
    assert "Sample Size:   6" in captured
    assert "Mean:          1.8333" in captured  # (1*2 + 2*3 + 3*1) / 6

    # 2. Verify the Stirling Distribution
    assert "{1: 2, 2: 3, 3: 1}" in captured

    # 3. Verify OEIS Bridge
    assert "OEIS:          A008275" in captured
    assert "Stirling numbers of first kind" in captured


def test_cli_stochastic_safety_valve(capsys):
    """Verify that N=100 without samples triggers the safety valve."""
    import pytest

    args = ["-n", "100"]

    with pytest.raises(SystemExit) as excinfo:
        run_analysis(args)

    assert excinfo.value.code == 1
    assert "avoid the heat death" in capsys.readouterr().out
