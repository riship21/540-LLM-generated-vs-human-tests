import subject

def test_flip_join_inputs_left_to_right():
    flip, how = subject.flip_join_inputs(True, "left")
    assert flip is True
    assert how == "right"
