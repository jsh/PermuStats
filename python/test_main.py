import pytest
import sys
from main import run_analysis

def test_exhaustive_n3_fixed_points(capsys, monkeypatch):
    test_args = ["main.py", "--n", "3", "--stat", "fixed-points"]
    monkeypatch.setattr(sys, "argv", test_args)
    run_analysis()
    captured = capsys.readouterr().out
    assert "OEIS Sequence: 2,3,0,1" in captured
    assert "Validation: True" in captured

def test_exhaustive_n3_cycle_lengths(capsys, monkeypatch):
    """
    N=3 cycle lengths:
    Cycles: {1: 2, 2: 3, 3: 1} -> OEIS: 0,2,3,1
    """
    test_args = ["main.py", "--n", "3", "--stat", "cycle-lengths"]
    monkeypatch.setattr(sys, "argv", test_args)
    
    run_analysis()
    
    captured = capsys.readouterr().out
    # Fix: Matching the '=' in output and the correct Stirling distribution
    assert "Stat=cycle-lengths" in captured
    assert "OEIS Sequence: 0,2,3,1" in captured
