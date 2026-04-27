import subject

def test_unescape_html_basic():
    assert subject.unescapeHTML("a &amp; b") == "a & b"
    assert subject.unescapeHTML("&lt;tag&gt;") == "<tag>"
    assert subject.unescapeHTML("&unknown;") == "&unknown;"
    assert subject.unescapeHTML(None) is None
