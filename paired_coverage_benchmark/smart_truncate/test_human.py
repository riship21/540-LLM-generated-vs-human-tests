import subject

def test_smart_truncate_no_max_length():
    txt = '1,000 reasons you are #1'
    assert subject.smart_truncate(txt) == txt
