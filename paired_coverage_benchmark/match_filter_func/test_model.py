from unittest.mock import patch
import pytest
import subject

@pytest.mark.parametrize(
    "filter_str, info_dict, match_str_return_value, expected_result",
    [
        ("keyword", {"title": "Matched Video", "id": "v1"}, True, None),
        ("bad_filter", {"title": "Unmatched Video", "id": "v2"}, False,
         "Unmatched Video does not pass filter bad_filter, skipping .."),
        ("another_bad", {"id": "v3"}, False,
         "v3 does not pass filter another_bad, skipping .."),
        ("no_info", {"duration": 100}, False,
         "video does not pass filter no_info, skipping .."),
        ("", {"title": "Any Video", "id": "v4"}, True, None),
        ("", {"title": "Another Video", "id": "v5"}, False,
         "Another Video does not pass filter , skipping .."),
    ]
)
def test_match_filter_func_behavior(filter_str, info_dict, match_str_return_value, expected_result):
    with patch('subject.match_str', return_value=match_str_return_value) as mock_match_str:
        _match_func = subject.match_filter_func(filter_str)
        result = _match_func(info_dict)
        assert result == expected_result
        mock_match_str.assert_called_once_with(filter_str, info_dict)
