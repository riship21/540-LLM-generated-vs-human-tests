import pytest
import subject

@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("foo", "foo"),
        ("Foo", "foo"),
        ("fOo", "foo"),
        ("foo.bar", "foo-bar"),
        ("Foo.Bar", "foo-bar"),
        ("Foo.....Bar", "foo-bar"),
        ("foo_bar", "foo-bar"),
        ("foo___bar", "foo-bar"),
        ("foo-bar", "foo-bar"),
        ("foo----bar", "foo-bar"),
    ],
)
def test_canonicalize_name(name: str, expected: str):
    assert subject.canonicalize_name(name) == expected
