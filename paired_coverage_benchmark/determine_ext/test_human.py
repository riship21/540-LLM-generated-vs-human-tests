import subject

def test_determine_ext_basic():
    assert subject.determine_ext("http://example.com/video.mp4") == "mp4"
    assert subject.determine_ext("http://example.com/video.mp4?download=true") == "mp4"
    assert subject.determine_ext("http://example.com/video.@@@") == "unknown_video"
    assert subject.determine_ext(None) == "unknown_video"
