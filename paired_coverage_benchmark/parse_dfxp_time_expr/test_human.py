import subject

def test_parse_dfxp_time_expr():
    assert subject.parse_dfxp_time_expr("10") == 10.0
    assert subject.parse_dfxp_time_expr("3.5") == 3.5
    assert subject.parse_dfxp_time_expr("7s") == 7.0
    assert subject.parse_dfxp_time_expr("") is None
    assert subject.parse_dfxp_time_expr("abc") is None
