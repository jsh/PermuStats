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
    assert "Distribution:" in captured

    # Correct distribution for all lengths found in S_3:
    # six 1-cycles, three 2-cycles, and two 3-cycles.
    assert "{1: 6, 2: 3, 3: 2}" in captured
