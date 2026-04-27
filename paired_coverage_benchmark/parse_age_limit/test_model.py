import pytest
import subject

@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        (None, None),
        ("7", 7),
        ("12", 12),
        ("18+", 18),
        ("0+", 0),
        ("99", 99),
        ("TV-Y7", 7),
        ("TV-MA", 18),
        ("PG-13", 13),
        ("invalid", None),
        ("123", None),
        ("7a", None),
        ("", None),
        ("+", None),
    ],
)
def test_parse_age_limit(input_string, expected_output):
    assert subject.parse_age_limit(input_string) == expected_output
