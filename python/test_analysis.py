import pytest
from analysis import Analyzer
from validation import validate_results, OEISLookup

def test_n3_analysis_and_search():
    # N=3 distribution: {0: 2, 1: 3, 3: 1}
    results = [0, 0, 1, 1, 1, 3]
    analyzer = Analyzer(results)
    dist = analyzer.frequency_distribution()
    
    # 1. Verify Stats
    assert analyzer.mean() == 1.0
    
    # 2. Verify Formatting
    seq_str = OEISLookup.format_sequence(3, dist)
    assert seq_str == "2,3,0,1"
    
    # 3. Verify Search (The Rencontres Number ID is A008290)
    result = OEISLookup.search(seq_str)
    if result and "error" not in result:
        assert "A008290" in result["id"]
        assert "Rencontres" in result["name"]

def test_n4_validation_logic():
    # N=4: 0:9, 1:8, 2:6, 3:0, 4:1 (Total 24)
    # This is the sequence for N=4 from OEIS A008290
    n4_dist = {0: 9, 1: 8, 2: 6, 3: 0, 4: 1}
    assert validate_results(4, n4_dist) is True
