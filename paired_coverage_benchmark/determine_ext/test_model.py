import subject

def test_determine_ext_with_trailing_slash_and_known_extension():
    url = "http://example.com/path/to/video.mp4/?quality=high"
    assert subject.determine_ext(url) == 'mp4'
