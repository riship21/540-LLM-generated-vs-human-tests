import subject

def test_match_filter_func_basic(monkeypatch):
    monkeypatch.setattr(subject, "match_str", lambda filter_str, info_dict: True)
    func = subject.match_filter_func("test")
    assert func({"title": "video1"}) is None

    monkeypatch.setattr(subject, "match_str", lambda filter_str, info_dict: False)
    func = subject.match_filter_func("test")
    result = func({"title": "video1"})
    assert "video1 does not pass filter test" in result
