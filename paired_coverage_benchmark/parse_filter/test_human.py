import tokenize
import subject

def test_parse_filter_basic():
    tokens = [
        (tokenize.NAME, "height", None, None, None),
        (tokenize.OP, ">", None, None, None),
        (tokenize.NUMBER, "720", None, None, None),
        (tokenize.OP, "]", None, None, None),
    ]
    assert subject.parse_filter(tokens) == "height>720"
