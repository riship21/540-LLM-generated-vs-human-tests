import subject

def test_convert_key_setter_returns_list():
    class Dummy:
        pass
    indexer = Dummy()
    key = (1, 2)
    result = subject._AtIndexer._convert_key(indexer, key, is_setter=True)
    assert result == [1, 2]
