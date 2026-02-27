import pytest
import sys
from main import run_analysis

def test_exhaustive_n3_cycle_counts(capsys, monkeypatch):
    # Ensure the list of strings is exactly what argparse expects
    test_args = ["main.py", "--n", "3", "--stat", "cycle-counts"]
    monkeypatch.setattr(sys, "argv", test_args)
    
    run_analysis()
    
    captured = capsys.readouterr().out
    assert "Stat=cycle-counts" in captured
    assert "OEIS Sequence: 0,2,3,1" in captured

def test_exhaustive_n3_cycle_lengths(capsys, monkeypatch):
    test_args = ["main.py", "--n", "3", "--stat", "cycle-lengths"]
    monkeypatch.setattr(sys, "argv", test_args)
    
    run_analysis()
    
    captured = capsys.readouterr().out
    assert "Stat=cycle-lengths" in captured
    # Update: Expect 'Distribution' instead of 'OEIS Sequence'
    assert "Distribution:" in captured
    assert "(3,): 2" in captured  # Verify actual data is present
