import pytest
from packaging.version import Version
import subject

@pytest.mark.parametrize(
    ("filename", "name", "version"),
    [
        ("foo-1.0.tar.gz", "foo", Version("1.0")),
        ("foo-1.0.zip", "foo", Version("1.0")),
    ],
)
def test_parse_sdist_filename(filename, name, version):
    assert subject.parse_sdist_filename(filename) == (name, version)
