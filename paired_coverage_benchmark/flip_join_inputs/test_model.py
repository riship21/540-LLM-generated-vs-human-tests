import pytest
import subject

@pytest.mark.parametrize(
    "self_is_mi, how_in, expected_flip_order, expected_how",
    [
        (False, "left", False, "left"),
        (False, "right", False, "right"),
        (False, "inner", False, "inner"),
        (False, "outer", False, "outer"),
        (True, "left", True, "right"),
        (True, "right", True, "left"),
        (True, "inner", True, "inner"),
        (True, "outer", True, "outer"),
        (True, "on", True, "on"),
    ],
)
def test_flip_join_inputs(self_is_mi, how_in, expected_flip_order, expected_how):
    flip_order, how_out = subject.flip_join_inputs(self_is_mi, how_in)
    assert flip_order == expected_flip_order
    assert how_out == expected_how
