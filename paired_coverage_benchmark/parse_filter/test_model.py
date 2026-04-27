import tokenize
import pytest
import subject

def _make_token(token_type, token_string):
    return (token_type, token_string, (1, 0), (1, len(token_string)), token_string)

@pytest.mark.parametrize(
    "tokens, expected_output",
    [
        ([
            _make_token(tokenize.NAME, 'column_name'),
            _make_token(tokenize.OP, '='),
            _make_token(tokenize.NUMBER, '100'),
            _make_token(tokenize.OP, ']'),
            _make_token(tokenize.NAME, 'ignored_part')
        ], 'column_name=100'),
        ([
            _make_token(tokenize.OP, ']'),
            _make_token(tokenize.NAME, 'some_name')
        ], ''),
        ([
            _make_token(tokenize.NAME, 'filter_field'),
            _make_token(tokenize.OP, '>'),
            _make_token(tokenize.STRING, "'value'"),
            _make_token(tokenize.OP, ']')
        ], "filter_field>'value'"),
        ([
            _make_token(tokenize.NAME, 'name'),
            _make_token(tokenize.OP, '.'),
            _make_token(tokenize.NAME, 'startswith'),
            _make_token(tokenize.OP, '('),
            _make_token(tokenize.STRING, "'prefix'"),
            _make_token(tokenize.OP, ')')
        ], None),
        ([], None),
    ]
)
def test_parse_filter_functionality(tokens, expected_output):
    assert subject.parse_filter(tokens) == expected_output
