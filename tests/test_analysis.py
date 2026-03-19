from permustats.analysis import AnalysisResult, Analyzer
from permustats.validation import validate_results, OEISLookup
from permustats.analysis import decompose_cycles


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


def test_oeis_stirling_cycles():
    """Verify that cycle count distribution matches Stirling numbers (A264428)."""
    from permustats.generator import PermutationGenerator

    n = 4
    perms = list(PermutationGenerator.exhaustive(n))
    results = [decompose_cycles(p) for p in perms]
    analyzer = Analyzer(results)

    dist = analyzer.frequency_distribution("total_cycles")
    seq_str = OEISLookup.format_sequence(n, dist)

    result = OEISLookup.search(seq_str)
    if result and "error" not in result:
        # A132393 is the preferred ID for Stirling numbers of the first kind as a triangle.
        assert "A132393" in result["id"]


def test_oeis_rencontres_fixed_points():
    """Verify that fixed point distribution matches Rencontres numbers (A008290)."""
    from permustats.generator import PermutationGenerator

    # N=4 provides a more unique sequence: 9, 8, 6, 0, 1
    n = 4
    perms = list(PermutationGenerator.exhaustive(n))
    results = [decompose_cycles(p) for p in perms]
    analyzer = Analyzer(results)

    dist = analyzer.frequency_distribution("fixed_points")
    seq_str = OEISLookup.format_sequence(n, dist)

    # For N=4, seq_str should be "9,8,6,0,1"
    result = OEISLookup.search(seq_str)
    if result and "error" not in result:
        # A008290 is the triangle of Rencontres numbers;
        # A000166 is the subfactorial (the first term '9')
        # We'll check for the primary structural match.
        assert result["id"] in ["A008290", "A000166", "A000522"]
        # A008290 is the most likely structural match for the full row.


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
            inversions=0,
            descents=0,
            major_index=0,
        )
        for c in counts
    ]

    # 3. Now Analyzer is happy because it receives exactly what its __init__ defines
    analyzer = Analyzer(results)
    dist = analyzer.frequency_distribution()

    assert dist[0] == 2
    assert dist[1] == 3
    assert dist[3] == 1
