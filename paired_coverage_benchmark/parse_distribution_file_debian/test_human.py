import subject

def test_parse_distribution_file_debian_ubuntu():
    result = subject.parse_distribution_file_Debian(
        None,
        name="test",
        data="Ubuntu 20.04 LTS",
        path="",
        collected_facts={'distribution_release': 'NA'}
    )
    assert result['distribution'] == 'Ubuntu'
