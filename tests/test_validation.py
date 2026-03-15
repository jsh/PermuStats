from __future__ import annotations
from unittest.mock import patch, MagicMock
from permustats.validation import ValidationTap, OEISLookup, validate_results
from permustats.models import AnalysisResult


def test_validate_results_logic():
    """Verify the combinatorial identity check helper using Fixed Points."""
    # N=3, S3 Fixed Point Distribution:
    # 0 pts: 2 perms, 1 pt: 3 perms, 2 pts: 0 perms, 3 pts: 1 perm
    fixed_point_dist = {0: 2, 1: 3, 2: 0, 3: 1}

    # Sum(freq) = 2+3+0+1 = 6 (3!)
    # Weighted Sum = (0*2 + 1*3 + 2*0 + 3*1) = 6 (3!)
    assert validate_results(3, fixed_point_dist) is True

    # Invalid distribution
    assert validate_results(3, {0: 1}) is False


def test_validation_tap_accumulation():
    """Ensure the tap aggregates metrics correctly across multiple observations."""
    tap = ValidationTap(n=3)
    # Manually create a result for (1)(2 3)
    res = AnalysisResult(
        permutation=[1, 3, 2],
        cycles=[[1], [3, 2]],
        total_cycles=2,
        fixed_points=1,
        cycle_lengths={1: 1, 2: 1},
        lengths_sequence=[1, 2],
    )

    tap.observe(res)
    tap.observe(res)  # Observe it twice

    assert tap.count == 2
    assert tap.total_cycles == 4
    assert tap.total_fixed_points == 2
    assert tap.length_counts[1] == 2
    assert tap.length_counts[2] == 2


@patch("requests.get")
def test_oeis_lookup_caching(mock_get, tmp_path):
    """Verify that OEISLookup handles network responses and uses the cache."""
    # Setup temporary cache file for testing to avoid touching real data
    cache_file = tmp_path / "test_cache.json"

    # We must patch the class attribute for the test
    with patch("permustats.validation.OEISLookup._cache_file", str(cache_file)):
        # Mock a successful OEIS response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [{"number": 8290, "name": "Rencontres numbers"}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # 1. First search (Network hit)
        res1 = OEISLookup.search("0,0,1")
        assert res1 is not None
        assert res1["id"] == "A008290"
        assert mock_get.call_count == 1

        # 2. Second search
        res2 = OEISLookup.search("0,0,1")
        assert res2 is not None  # This 'guards' the next line for the type-checker
        assert res2["id"] == "A008290"
        assert mock_get.call_count == 1
