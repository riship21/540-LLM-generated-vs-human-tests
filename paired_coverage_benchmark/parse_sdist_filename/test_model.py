from packaging.version import Version
import subject

def test_parse_sdist_filename_valid_tar_gz():
    filename = "My_Package-1.2.3.tar.gz"
    expected_name = subject.canonicalize_name("My_Package")
    expected_version = Version("1.2.3")
    name, version = subject.parse_sdist_filename(filename)
    assert name == expected_name
    assert version == expected_version
