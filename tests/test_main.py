from permustats.main import run_analysis


def test_exhaustive_n3_cycle_counts(capsys):
    # Pass the arguments as a list of strings
    test_args = ["-n", "3", "-t", "cycle-counts"]

    # Simulate: permustats -n 3 -t cycle_counts
    # (Since N! = 6, it will trigger the exhaustive logic automatically)
    run_analysis(test_args)

    captured = capsys.readouterr().out
    assert "Stat=cycle-counts" in captured
    assert "OEIS Sequence: 0,2,3,1" in captured


def test_exhaustive_n3_cycle_lengths(capsys):
    test_args = ["-n", "3", "--stat", "cycle-lengths"]

    run_analysis(test_args)

    captured = capsys.readouterr().out
    assert "Stat=cycle-lengths" in captured
    # Update: Expect 'Distribution' instead of 'OEIS Sequence'
    assert "Distribution:" in captured
    assert "(3,): 2" in captured  # Verify actual data is present
