import pytest

from permustats.analysis import AnalysisResult, Analyzer
from permustats.validation import validate_results, OEISLookup
from permustats.analysis import decompose_cycles
from permustats.math_utils import harmonic_number


def test_cycle_decomposition_identity():
    # Identity [1, 2, 3] -> (1)(2)(3)
    res = decompose_cycles([1, 2, 3])
    assert res.total_cycles == 3
    assert res.fixed_points == 3
    assert res.cycle_lengths == {1: 3}


def test_cycle_decomposition_full_cycle():
    # Full cycle [2, 3, 1] -> (1 2 3)
    res = decompose_cycles([2, 3, 1])
    assert res.total_cycles == 1
    assert res.fixed_points == 0
    assert res.cycle_lengths == {3: 1}


def test_cycle_decomposition_mixed():
    # [2, 1, 3, 5, 4] -> (1 2)(3)(4 5)
    res = decompose_cycles([2, 1, 3, 5, 4])
    assert res.total_cycles == 3
    assert res.fixed_points == 1
    assert res.cycle_lengths == {2: 2, 1: 1}


def test_n3_analysis_and_search():
    # Hard-coded permutations for N=3 (The full S3 group)
    s3_permutations = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

    # 1. Map the raw lists into AnalysisResult objects
    results = [decompose_cycles(p) for p in s3_permutations]

    # 2. Now the Analyzer is perfectly happy with the types
    analyzer = Analyzer(results)
    dist = analyzer.frequency_distribution()

    # 3. Verify Stats
    # The mean of total cycles for all permutations of N is ALWAYS H_n
    assert analyzer.mean() == pytest.approx(harmonic_number(3))
    # or simply
    assert analyzer.mean() == pytest.approx(1.8333333333)
    # [3, 2, 1] -> 3 cycles, 2 cycles (3 of them), 1 cycle (2 of them)
    # Stirling Numbers [3, 1]=2, [3, 2]=3, [3, 3]=1
    assert dist[1] == 2
    assert dist[2] == 3
    assert dist[3] == 1

    # 4. Verify Formatting
    seq_str = OEISLookup.format_sequence(3, dist)
    assert seq_str == "0,2,3,1"

    # 5. Verify Search (The Rencontres Number ID is A008290)
    result = OEISLookup.search(seq_str)
    if result and "error" not in result:
        assert "A008290" in result["id"]
        assert "Rencontres" in result["name"]


def test_n4_validation_logic():
    # N=4: 0:9, 1:8, 2:6, 3:0, 4:1 (Total 24)
    # This is the sequence for N=4 from OEIS A008290
    n4_dist = {0: 9, 1: 8, 2: 6, 3: 0, 4: 1}
    assert validate_results(4, n4_dist) is True


def test_analyzer_frequency_distribution():
    # 1. Take the raw counts
    counts = [0, 0, 1, 1, 1, 3]

    # 2. CONVERT them into a list of AnalysisResult objects
    # This is the step that turns the list[int] into a list[AnalysisResult]
    results = [
        AnalysisResult(
            permutation=[1],
            cycles=[[1]],
            total_cycles=c,
            fixed_points=0,
            cycle_lengths={},
            lengths_sequence=[],
        )
        for c in counts
    ]

    # 3. Now Analyzer is happy because it receives exactly what its __init__ defines
    analyzer = Analyzer(results)
    dist = analyzer.frequency_distribution()

    assert dist[0] == 2
    assert dist[1] == 3
    assert dist[3] == 1
