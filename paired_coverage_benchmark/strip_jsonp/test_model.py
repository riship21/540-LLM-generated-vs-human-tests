import subject

def test_strip_jsonp_standard_case():
    code = 'myCallback({"data": "example", "status": "success"});'
    assert subject.strip_jsonp(code) == '{"data": "example", "status": "success"}'
