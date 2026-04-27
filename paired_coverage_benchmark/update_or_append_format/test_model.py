import subject

def test_appends_new_format_from_dict_and_updates():
    initial_formats = []
    formats_dict = {
        101: {"format_id": 101, "codec": "h264", "resolution": "1920x1080"}
    }
    representation_id_to_add = 101
    update_data = {"bitrate": "5Mbps", "duration": "PT60S"}

    result_formats = subject.update_or_append_format(
        initial_formats, formats_dict, representation_id_to_add, update_data
    )

    expected_format = {
        "format_id": 101,
        "codec": "h264",
        "resolution": "1920x1080",
        "bitrate": "5Mbps",
        "duration": "PT60S",
    }

    assert len(result_formats) == 1
    assert result_formats[0] == expected_format
    assert initial_formats is result_formats
