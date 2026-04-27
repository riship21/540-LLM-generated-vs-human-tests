import subject

def test_strip_jsonp_basic():
    assert subject.strip_jsonp('callback({"a":1});') == '{"a":1}'
    assert subject.strip_jsonp('cb ( {"b":2} ) ;') == '{"b":2}'
    assert subject.strip_jsonp('cb({"c":3}); // comment') == '{"c":3}'
    assert subject.strip_jsonp('{"d":4}') == '{"d":4}'
