import os
import subject

def test_validate_collection_path():
    assert os.path.normpath(subject.validate_collection_path("/tmp")) == os.path.normpath("/tmp/ansible_collections")
    assert os.path.normpath(subject.validate_collection_path("/tmp/ansible_collections")) == os.path.normpath("/tmp/ansible_collections")
    assert os.path.normpath(subject.validate_collection_path("/home/user")) == os.path.normpath("/home/user/ansible_collections")
