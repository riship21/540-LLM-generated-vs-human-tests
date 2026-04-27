import subject

def test_smart_truncate_word_boundary_and_save_order_interaction():
    text_diff = "alpha bravo charlie_very_long delta"
    max_len_diff = 17
    separator_diff = " "

    assert subject.smart_truncate(
        text_diff,
        max_len_diff,
        word_boundary=True,
        separator=separator_diff,
        save_order=True,
    ) == "alpha bravo"

    assert subject.smart_truncate(
        text_diff,
        max_len_diff,
        word_boundary=True,
        separator=separator_diff,
        save_order=False,
    ) == "alpha bravo delta"
