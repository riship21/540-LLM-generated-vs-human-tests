import subject

class FakeLoader:
    def __init__(self, default_collection):
        self.default_collection = default_collection

def test_ensure_default_collection_basic(monkeypatch):
    monkeypatch.setattr(subject, 'AnsibleCollectionLoader', lambda: FakeLoader('my.collection'))
    result = subject._ensure_default_collection(None)
    assert result[0] == 'my.collection'
    assert 'ansible.legacy' in result

    result = subject._ensure_default_collection(['custom.collection'])
    assert result[0] == 'my.collection'
    assert 'custom.collection' in result

    result = subject._ensure_default_collection(['my.collection'])
    assert result.count('my.collection') == 1
