import pytest
import subject

@pytest.mark.parametrize(
    "data_input, expected_output",
    [
        ("This is some Debian distribution data.", {'distribution': 'Debian'}),
        ("This is some Raspbian distribution data.", {'distribution': 'Debian'}),
        ("This is some Ubuntu distribution data.", {'distribution': 'Ubuntu'}),
        ("This is some SteamOS distribution data.", {'distribution': 'SteamOS'}),
        ("Generic Linux distribution info.", {}),
        ("Debian and Ubuntu in the same string.", {'distribution': 'Debian'}),
        ("", {}),
    ]
)
def test_parse_distribution_file_Debian(data_input, expected_output):
    result = subject.parse_distribution_file_Debian(None, "test_name", data_input, "test_path", {})
    assert result == expected_output
