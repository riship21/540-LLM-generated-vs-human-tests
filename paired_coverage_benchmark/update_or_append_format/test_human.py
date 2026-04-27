import subject

def test_update_or_append_format_basic():
    formats = []
    formats_dict = {"vid1": {"format_id": "vid1", "ext": "mp4"}}
    f = {"format_id": "vid1", "url": "test_url"}
    result = subject.update_or_append_format(formats, formats_dict, "vid1", f)
    assert len(result) == 1
    assert result[0]["url"] == "test_url"

    f_update = {"format_id": "vid1", "height": 720}
    result = subject.update_or_append_format(result, formats_dict, "vid1", f_update)
    assert len(result) == 1
    assert result[0]["height"] == 720
