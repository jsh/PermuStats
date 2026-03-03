import pytest
from permustats.math_utils import harmonic_number, subfactorial, stirling_first


def test_harmonic_numbers():
    assert harmonic_number(0) == 0.0
    assert harmonic_number(1) == 1.0
    assert harmonic_number(2) == 1.5
    assert harmonic_number(4) == pytest.approx(2.0833333333)


def test_subfactorials():
    # !n: 1, 0, 1, 2, 9, 44...
    assert subfactorial(0) == 1
    assert subfactorial(1) == 0
    assert subfactorial(2) == 1
    assert subfactorial(3) == 2
    assert subfactorial(4) == 9
    assert subfactorial(6) == 265


def test_stirling_numbers():
    # [3, 2] = 3
    # [4, 2] = 11
    assert stirling_first(3, 2) == 3
    assert stirling_first(4, 2) == 11
    assert stirling_first(5, 3) == 35
    assert stirling_first(6, 1) == 120  # (6-1)!
