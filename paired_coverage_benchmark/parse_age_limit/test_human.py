import subject

def test_parse_age_limit_basic():
    assert subject.parse_age_limit("18") == 18
    assert subject.parse_age_limit("13+") == 13
    assert subject.parse_age_limit("R") == 16
    assert subject.parse_age_limit(None) is None
    assert subject.parse_age_limit("UNKNOWN") is None
