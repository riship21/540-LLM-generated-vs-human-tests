import pytest
import subject

@pytest.mark.parametrize(
    "key_input, is_setter, expected_output",
    [
        ("test_string", False, "test_string"),
        ("string_key", True, ['s', 't', 'r', 'i', 'n', 'g', '_', 'k', 'e', 'y']),
        ((1, 2, 3), True, [1, 2, 3]),
        ([4, 5, 6], True, [4, 5, 6]),
    ]
)
def test_convert_key_behavior(key_input, is_setter, expected_output):
    actual_output = subject._AtIndexer._convert_key(None, key_input, is_setter)
    assert actual_output == expected_output
    if is_setter and isinstance(key_input, list):
        assert actual_output is not key_input
