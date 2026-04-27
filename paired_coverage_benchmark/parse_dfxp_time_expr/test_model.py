import subject

def test_parse_dfxp_time_expr_leading_decimal_point():
    assert subject.parse_dfxp_time_expr('.5s') == 0.5

def test_parse_dfxp_time_expr_leading_decimal_point_no_s():
    assert subject.parse_dfxp_time_expr('.75') == 0.75

def test_parse_dfxp_time_expr_basic():
    assert subject.parse_dfxp_time_expr('10') == 10.0
    assert subject.parse_dfxp_time_expr('10s') == 10.0
    assert subject.parse_dfxp_time_expr('10.5') == 10.5
    assert subject.parse_dfxp_time_expr('10.5s') == 10.5
    assert subject.parse_dfxp_time_expr('0') == 0.0
    assert subject.parse_dfxp_time_expr('0.0s') == 0.0

def test_parse_dfxp_time_expr_invalid():
    assert subject.parse_dfxp_time_expr('') is None
    assert subject.parse_dfxp_time_expr(None) is None
    assert subject.parse_dfxp_time_expr('abc') is None
    assert subject.parse_dfxp_time_expr('10m') is None
    assert subject.parse_dfxp_time_expr('10.s') is None
    assert subject.parse_dfxp_time_expr('10..5s') is None
