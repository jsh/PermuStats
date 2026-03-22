import pytest
from permustats.main import run_analysis


def test_exhaustive_n3_cycle_counts(capsys):
    """Legacy check: Verify N=3 cycle counts header and distribution."""
    test_args = ["-n", "3", "-t", "cycle-counts"]
    run_analysis(test_args)

    captured = capsys.readouterr().out
    # 1. Check Header (Legacy requirement)
    assert "Stat=cycle-counts" in captured
    # 2. Check Distribution (A008275: Stirling numbers 1st kind)
    assert "{1: 2, 2: 3, 3: 1}" in captured
    assert "OEIS:          A008275" in captured


def test_exhaustive_n3_cycle_lengths(capsys):
    """Legacy check: Verify cycle lengths distribution for S_3."""
    test_args = ["-n", "3", "--stat", "cycle-lengths"]
    run_analysis(test_args)

    captured = capsys.readouterr().out
    assert "Stat=cycle-lengths" in captured
    # S_3 has six 1-cycles, three 2-cycles, and two 3-cycles
    assert "{1: 6, 2: 3, 3: 2}" in captured


def test_safety_valve_trigger(capsys):
    """New Requirement: Verify the 'Periculum' check for N > 11 without samples."""
    test_args = ["-n", "12"]  # No -s/--samples provided

    with pytest.raises(SystemExit) as excinfo:
        run_analysis(test_args)

    assert excinfo.value.code == 1
    captured = capsys.readouterr().out
    assert "avoid the heat death" in captured


def test_cli_validation_smoke_test(capsys):
    """New Requirement: Verify that --validate triggers the ValidationTap report."""
    args = ["-n", "3", "--stat", "cycle-counts", "--validate"]
    run_analysis(args)

    captured = capsys.readouterr().out
    assert "🛡️ Validation Report" in captured


@pytest.mark.parametrize(
    "stat, expected_oeis",
    [
        ("descents", "A008292"),
        ("inversions", "A008302"),
    ],
)
def test_cli_identities_n4(capsys, stat, expected_oeis):
    """New Requirement: Verify Eulerian and Mahonian identities for N=4."""
    test_args = ["-n", "4", "--stat", stat]
    run_analysis(test_args)

    captured = capsys.readouterr().out
    assert f"Stat={stat}" in captured
    assert f"OEIS:          {expected_oeis}" in captured

    if stat == "descents":
        # Variance for Eulerian N=4 is 10/24 ~ 0.4167
        assert "Variance:      0.4167" in captured
    elif stat == "inversions":
        # Variance for Mahonian N=4 is 130/60? No, 2.1667.
        assert "Variance:      2.1667" in captured
